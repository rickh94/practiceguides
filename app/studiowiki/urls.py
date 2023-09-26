"""studiowiki URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from wiki.sitemap import (
    BasicSitemap,
    ComposersSitemap,
    PiecesSitemap,
    SkillsSitemap,
    SpotsSitemap,
    StandaloneExercisesSitemap,
)

sitemaps = {
    "basic": BasicSitemap,
    "pieces": PiecesSitemap,
    "standalone_exercises": StandaloneExercisesSitemap,
    "composers": ComposersSitemap,
    "skills": SkillsSitemap,
    "spots": SpotsSitemap,
}

urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("wiki.urls")),
    path("admin/", admin.site.urls),
    path("pauth/", include("passkey_auth.urls")),
] + static(settings.MEDIA_PATH, document_root=settings.MEDIA_ROOT)
