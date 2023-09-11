from django.contrib import admin
from django.utils.html import format_html

from . import models

# Register your models here.
admin.site.register(models.Composer)
admin.site.register(models.Book)
admin.site.register(models.Spot)
admin.site.register(models.Step)
admin.site.register(models.Skill)
admin.site.register(models.Piece)
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


admin.site.register(models.Recording, RecordingAdmin)
