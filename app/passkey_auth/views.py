import base64
import datetime

import webauthn
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (HttpRequest, HttpResponse, HttpResponseBadRequest,
                         HttpResponseServerError)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from webauthn.helpers.exceptions import InvalidRegistrationResponse
from webauthn.helpers.structs import (AuthenticatorSelectionCriteria,
                                      PublicKeyCredentialDescriptor,
                                      RegistrationCredential,
                                      UserVerificationRequirement)

from .models import PasskeyCredential
from .types import AuthenticatedHttpRequest


@require_GET
@login_required
def user_profile(request: HttpRequest) -> HttpResponse:
    if request.htmx and not request.htmx.boosted:
        return render(request, "htmx/user_profile.html")
    return render(request, "user_profile.html", {})


@require_GET
@login_required
def start_passkey_registration(request: AuthenticatedHttpRequest) -> HttpResponse:
    if not settings.WEBAUTHN_RP_ID or not settings.WEBAUTHN_SERVER_NAME:
        return HttpResponseServerError("Missing settings")
    pcco = webauthn.generate_registration_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        rp_name=settings.WEBAUTHN_SERVER_NAME,
        user_id=str(request.user.id),
        user_name=str(request.user.username),
        user_display_name=str(request.user),
        authenticator_selection=AuthenticatorSelectionCriteria(
            user_verification=UserVerificationRequirement.REQUIRED
        ),
    )
    challenge = base64.b64encode(pcco.challenge).decode("utf-8")
    request.session["registration_state"] = {
        "challenge": challenge,
        "created": datetime.datetime.now().timestamp(),
    }

    return HttpResponse(webauthn.options_to_json(pcco), content_type="application/json")


@require_POST
@csrf_exempt
@login_required
def finish_passkey_registration(request: AuthenticatedHttpRequest) -> HttpResponse:
    registration_credential = RegistrationCredential.parse_raw(request.body)

    try:
        challenge_info = request.session["registration_state"]
        if (
            datetime.datetime.fromtimestamp(challenge_info["created"])
            + datetime.timedelta(minutes=5)
            < datetime.datetime.now()
        ):
            request.session["registration_state"] = None
            return HttpResponseBadRequest("Expired Challenge")
        expected = base64.b64decode(challenge_info["challenge"])
        if not settings.WEBAUTHN_RP_ID or not settings.WEBAUTHN_ORIGIN:
            return HttpResponseServerError("Missing settings")
        verification = webauthn.verify_registration_response(
            credential=registration_credential,
            expected_challenge=expected,
            expected_rp_id=settings.WEBAUTHN_RP_ID,
            expected_origin=settings.WEBAUTHN_ORIGIN,
        )
    except InvalidRegistrationResponse as e:
        print(e)
        return HttpResponseBadRequest("Invalid registration response")

    credential = PasskeyCredential(
        user=request.user,
        credential_id=verification.credential_id,
        credential_public_key=verification.credential_public_key,
        current_sign_count=0,
    )
    credential.save()

    return HttpResponse(b"Passkey Created")


@require_POST
@csrf_exempt
def start_passkey_login(request: HttpRequest) -> HttpResponse:
    username = request.POST.get("username")
    if not username or type(username) != str:
        return HttpResponseBadRequest(b"Username required")
    try:
        user: User = User.objects.get(username=username.lower().strip())
    except User.DoesNotExist:
        return HttpResponseBadRequest(b"Cannot log in with username")
    allowed_credentials = [
        PublicKeyCredentialDescriptor(id=credential.credential_id)
        for credential in user.credentials.all()
    ]

    if not settings.WEBAUTHN_RP_ID:
        return HttpResponseServerError(b"Missing settings")

    authentication_options = webauthn.generate_authentication_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        allow_credentials=allowed_credentials,
        user_verification=UserVerificationRequirement.REQUIRED,
    )

    request.session["auth_state"] = {
        "challenge": base64.b64encode(authentication_options.challenge).decode("utf-8"),
        "created": datetime.datetime.now().timestamp(),
        "user_id": user.pk,
    }

    return HttpResponse(
        webauthn.options_to_json(authentication_options),
        content_type="application/json",
    )


@require_POST
@csrf_exempt
def finish_passkey_login(request: HttpRequest) -> HttpResponse:
    user = authenticate(request)
    if user is not None:
        messages.success(request, "Login successful")
        login(request, user)
        return HttpResponse("Login successful")
    else:
        messages.error(request, "Login failed")
        return HttpResponseBadRequest("Login Failed")
