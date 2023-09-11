from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.user_profile, name="user_profile"),
    path(
        "start-registration/",
        views.start_passkey_registration,
        name="start_passkey_registration",
    ),
    path(
        "finish-registration/",
        views.finish_passkey_registration,
        name="finish_passkey_registration",
    ),
    path("start-login/", views.start_passkey_login, name="start_passkey_login"),
    path("finish-login/", views.finish_passkey_login, name="finish_passkey_login"),
]
