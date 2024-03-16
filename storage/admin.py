from django.contrib import admin

from storage import models


@admin.register(models.Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ("title", "owner")
    search_fields = ("title", )


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "status", "duration", "original_language", "translate_to")
    search_fields = ("title", )
    list_filter = ("status", "original_language", "translate_to")


@admin.register(models.Speech)
class SpeechAdmin(admin.ModelAdmin):
    list_display = ("content", "speaker", "from_time", "to_time", "text")
    search_fields = ("content__title", )
