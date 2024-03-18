from django.contrib import admin

from storage import models


@admin.register(models.Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ("title", "owner")
    search_fields = ("title", )


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "folder", "status", "duration", "original_language", "translate_to", "updated_at")
    search_fields = ("title", )
    list_filter = ("status", "original_language", "translate_to", "updated_at", "created_at")


@admin.register(models.Speech)
class SpeechAdmin(admin.ModelAdmin):
    list_display = ("text", "content", "speaker", "from_time", "to_time")
    search_fields = ("content__title", )
