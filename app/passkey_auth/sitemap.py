from django.contrib import sitemaps
from django.urls import reverse


class PAuthSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ["start_passkey_registration", "start_passkey_login"]

    def location(self, item):
        return reverse(item)
