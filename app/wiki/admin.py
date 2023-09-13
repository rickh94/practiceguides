from django.conf.urls.static import static
from django.contrib import admin
from django.utils.html import format_html

from . import models

# Register your models here.
admin.site.register(models.Composer)
admin.site.register(models.Book)
admin.site.register(models.Skill)
admin.site.register(models.PieceExercise)
admin.site.register(models.StandaloneExercise)


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


class SpotAdmin(admin.ModelAdmin, RecordingPlayerMixin):
    list_display = ["nickname", "piece", "order", "description"]
    readonly_fields = ["player"]
    change_form_template = "wiki/admin/abcjs_change_form.html"


class StepAdmin(admin.ModelAdmin, RecordingPlayerMixin):
    list_display = ["spot", "order", "instructions", "player"]
    readonly_fields = ["player"]
    change_form_template = "wiki/admin/abcjs_change_form.html"


class PieceAdmin(admin.ModelAdmin, RecordingPlayerMixin):
    list_display = ["title", "composer", "description", "order"]
    readonly_fields = ["player"]
    change_form_template = "wiki/admin/abcjs_change_form.html"


admin.site.register(models.Recording, RecordingAdmin)
admin.site.register(models.Spot, SpotAdmin)
admin.site.register(models.Step, StepAdmin)
admin.site.register(models.Piece, PieceAdmin)
