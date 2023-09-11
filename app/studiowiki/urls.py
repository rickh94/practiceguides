"""studiowiki URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("wiki.urls")),
    path("admin/", admin.site.urls),
    path("pauth/", include("passkey_auth.urls")),
] + static(settings.MEDIA_PATH, document_root=settings.MEDIA_ROOT)
