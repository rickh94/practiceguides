from django.contrib import sitemaps
from django.urls import reverse

from .models import Composer, Piece, Skill, Spot, StandaloneExercise


class BasicSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return [
            "index",
            "piece_list",
            "skill_list",
            "book_list",
            "standaloneexercise_list",
            "composer_list",
            "search",
        ]

    def location(self, item):
        return reverse(item)


class PiecesSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return Piece.objects.all()


class StandaloneExercisesSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return StandaloneExercise.objects.all()


class SkillsSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return Skill.objects.all()


class ComposersSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return Composer.objects.all()


class SpotsSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return Spot.objects.all()
