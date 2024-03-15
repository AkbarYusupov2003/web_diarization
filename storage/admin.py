from django.contrib import admin

from storage import models


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("owner", "title", "audio", "language", "duration", "status")
    search_fields = ("title", )
    list_filter = ("status", "language")


@admin.register(models.Speech)
class SpeechAdmin(admin.ModelAdmin):
    list_display = ("content", "speaker", "from_time", "to_time", "text")
    search_fields = ("content__title", )
