from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from . import models
from .util import truncate_words

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


class RecordingPlayerMixin:
    def player(self, obj):
        if obj.recording and obj.recording.file.url:
            return format_html(
                '<audio controls><source src="{0}" type="audio/mpeg"></audio>',
                obj.recording.file.url,
            )

    player.allow_tags = True
    player.__name__ = "Current Audio"


class TruncatedDescriptionMixin:
    def truncated_description(self, obj):
        return truncate_words(obj.description, 10)

    truncated_description.__name__ = "Description"


@admin.register(models.Recording)
class RecordingAdmin(ModelAdmin):
    list_display = ["name", "description", "player"]
    readonly_fields = ["player"]
    search_fields = ["name"]

    def player(self, obj):
        if obj.file.url:
            return format_html(
                '<audio controls><source src="{0}" type="audio/mpeg"></audio>',
                obj.file.url,
            )

    player.allow_tags = True
    player.__name__ = "Current Audio"


@admin.register(models.Spot)
class SpotAdmin(ModelAdmin, RecordingPlayerMixin, TruncatedDescriptionMixin):
    list_display = [
        "nickname",
        "piece",
        "order",
        "truncated_description",
        "player",
    ]
    list_filter = ["piece", "skills__name"]
    autocomplete_fields = ["recording", "piece"]
    readonly_fields = ["player"]
    change_form_template = "wiki/admin/abcjs_change_form.html"
    search_fields = [
        "piece__title",
        "nickname",
        "piece__composer__name",
        "skills__name",
    ]


@admin.register(models.PieceExercise)
class PieceExerciseAdmin(ModelAdmin, RecordingPlayerMixin, TruncatedDescriptionMixin):
    list_display = ["nickname", "piece", "truncated_description"]
    list_filter = ["piece"]
    autocomplete_fields = ["recording", "piece"]
    readonly_fields = ["player"]
    change_form_template = "wiki/admin/abcjs_change_form.html"
    search_fields = [
        "piece__title",
        "nickname",
        "skills__name",
        "piece__composer__name",
    ]


@admin.register(models.Piece)
class PieceAdmin(ModelAdmin, RecordingPlayerMixin, TruncatedDescriptionMixin):
    list_display = ["title", "composer", "truncated_description", "order"]
    readonly_fields = ["player"]
    list_filter = ["composer", "book", "skills"]
    search_fields = ["title", "composer__name", "skills__name"]
    autocomplete_fields = ["composer", "book", "recording"]
    # change_form_template = "wiki/admin/abcjs_change_form.html"


@admin.register(models.StandaloneExercise)
class StandaloneExerciseAdmin(
    ModelAdmin, RecordingPlayerMixin, TruncatedDescriptionMixin
):
    list_display = ["title", "composer", "truncated_description", "order"]
    list_filter = ["composer", "book", "skills"]
    readonly_fields = ["player"]
    search_fields = ["title", "composer__name", "skills__name", "book__title"]
    autocomplete_fields = ["composer", "book", "recording"]


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin, TruncatedDescriptionMixin):
    list_display = ["title", "composer", "truncated_description"]
    search_fields = ["title", "composer__name"]
    autocomplete_fields = ["composer"]


@admin.register(models.Skill)
class SkillAdmin(ModelAdmin, TruncatedDescriptionMixin):
    list_display = ["name", "truncated_description"]
    list_filter = ["piece", "spot", "pieceexercise", "standaloneexercise"]
    search_fields = ["name", "piece__title", "piece__composer__name"]


@admin.register(models.Composer)
class ComposerAdmin(ModelAdmin):
    list_display = ["name"]
    list_filter = ["pieces", "books", "standaloneexercises"]
    search_fields = ["name", "pieces__title"]


admin.site.site_header = "Studio Wiki Admin"
admin.site.site_title = "Studio Wiki Admin"
admin.site.index_title = "Welcome to Studio Wiki Admin"
