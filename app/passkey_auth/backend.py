import base64
import datetime
from typing import Any, Optional

import webauthn
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.http import HttpRequest
from passkey_auth.models import PasskeyCredential
from pydantic import ValidationError
from webauthn.helpers.exceptions import InvalidAuthenticationResponse
from webauthn.helpers.structs import AuthenticationCredential


class PasskeyBackend(BaseBackend):
    """
    Authenticate against passkey credentials.
    """

    def authenticate(
        self, request: Optional[HttpRequest], **kwargs: Any
    ) -> User | None:
        if not request:
            return None
        auth_state = request.session.get("auth_state")
        if not auth_state:
            return None
        try:
            submitted_credential = AuthenticationCredential.parse_raw(request.body)
        except ValidationError:
            return None
        if (
            datetime.datetime.fromtimestamp(auth_state["created"])
            + datetime.timedelta(minutes=5)
            < datetime.datetime.now()
        ):
            request.session["auth_state"] = None
            return None

        try:
            user = User.objects.get(pk=auth_state["user_id"])
        except User.DoesNotExist:
            return None

        stored_credential: PasskeyCredential = user.credentials.get(
            credential_id=webauthn.base64url_to_bytes(submitted_credential.id),
        )

        expected_challenge = base64.b64decode(auth_state["challenge"])

        if not settings.WEBAUTHN_ORIGIN or not settings.WEBAUTHN_RP_ID:
            return None

        try:
            webauthn.verify_authentication_response(
                credential=submitted_credential,
                expected_challenge=expected_challenge,
                expected_origin=settings.WEBAUTHN_ORIGIN,
                expected_rp_id=settings.WEBAUTHN_RP_ID,
                credential_public_key=stored_credential.credential_public_key,
                credential_current_sign_count=0,
            )
            request.session["auth_state"] = None
            return user
        except InvalidAuthenticationResponse:
            return None

    def get_user(self, user_id: int) -> User | None:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
