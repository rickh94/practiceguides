from django.contrib import admin
from django.utils.html import format_html

from . import models
from .util import truncate_words


class RecordingAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "player"]
    readonly_fields = ["player"]

    def player(self, obj):
        if obj.file.url:
            return format_html(
                '<audio controls><source src="{0}" type="audio/mpeg"></audio>',
                obj.file.url,
            )

    player.allow_tags = True
    player.__name__ = "Current Audio"


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


class SpotAdmin(admin.ModelAdmin, RecordingPlayerMixin, TruncatedDescriptionMixin):
    list_display = ["nickname", "piece", "order", "truncated_description", "player"]
    list_filter = ["piece"]
    readonly_fields = ["player"]
    change_form_template = "wiki/admin/abcjs_change_form.html"


class PieceExerciseAdmin(
    admin.ModelAdmin, RecordingPlayerMixin, TruncatedDescriptionMixin
):
    list_display = ["nickname", "piece", "truncated_description"]
    list_filter = ["piece"]
    readonly_fields = ["player"]
    change_form_template = "wiki/admin/abcjs_change_form.html"


# TODO: suggest next step number in the admin or set it automatically


class StepAdmin(admin.ModelAdmin, RecordingPlayerMixin):
    list_display = ["spot", "order", "truncated_instructions", "player"]
    list_filter = ["spot__piece", "spot"]
    readonly_fields = ["player"]
    change_form_template = "wiki/admin/abcjs_change_form.html"

    def truncated_instructions(self, obj):
        return truncate_words(obj.instructions)

    truncated_instructions.__name__ = "Instructions"


class PieceAdmin(admin.ModelAdmin, RecordingPlayerMixin, TruncatedDescriptionMixin):
    list_display = ["title", "composer", "truncated_description", "order"]
    readonly_fields = ["player"]
    list_filter = ["composer", "book", "skills"]
    # change_form_template = "wiki/admin/abcjs_change_form.html"


class StandaloneExerciseAdmin(
    admin.ModelAdmin, RecordingPlayerMixin, TruncatedDescriptionMixin
):
    list_display = ["title", "composer", "truncated_description", "order"]
    list_filter = ["composer", "book", "skills"]
    readonly_fields = ["player"]


class BookAdmin(admin.ModelAdmin, TruncatedDescriptionMixin):
    list_display = ["title", "composer", "truncated_description"]


class SkillAdmin(admin.ModelAdmin, TruncatedDescriptionMixin):
    list_display = ["name", "truncated_description"]
    list_filter = ["piece", "spot", "pieceexercise", "standaloneexercise"]


class ComposerAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["pieces", "books", "standaloneexercises"]


admin.site.register(models.Recording, RecordingAdmin)
admin.site.register(models.Spot, SpotAdmin)
admin.site.register(models.Step, StepAdmin)
admin.site.register(models.Piece, PieceAdmin)
admin.site.register(models.StandaloneExercise, StandaloneExerciseAdmin)
admin.site.register(models.PieceExercise, PieceExerciseAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Skill, SkillAdmin)
admin.site.register(models.Composer, ComposerAdmin)
