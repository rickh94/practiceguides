"""studiowiki URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.urls import include, path
from django.views.generic import RedirectView
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

favicon_view = RedirectView.as_view(url="/static/icons/favicon.ico", permanent=True)


def robots(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        f"""User-agent: *
Disallow: /

Sitemap: https://{request.get_host()}/sitemap.xml
    """,
        content_type="text/plain",
    )


urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("wiki.urls")),
    path("admin/", admin.site.urls),
    path("favicon.ico", favicon_view),
    path("robots.txt", robots),
] + static(settings.MEDIA_PATH, document_root=settings.MEDIA_ROOT)
