from django.contrib.auth import get_user_model
from django.db import models


class Folder(models.Model):
    owner = models.ForeignKey(
        get_user_model(), verbose_name="Владелец", on_delete=models.CASCADE, related_name="folders"
    )
    title = models.CharField("Название", max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Папка"
        verbose_name_plural = "Папки"


class Content(models.Model):
    # https://github.com/openai/whisper
    class StatusChoices(models.TextChoices):
        queue = "QUEUE", "В очереди"
        diarizing = "DIARIZING", "Диаризация"
        transcribing = "TRANSCRIBING", "Транскрипция"
        translating = "TRANSLATING", "Перевод"
        processed = "PROCESSED", "Выполнен"
        failed = "FAILED", "Ошибка"

    owner = models.ForeignKey(
        get_user_model(), verbose_name="Владелец", on_delete=models.CASCADE, related_name="contents"
    )
    folder = models.ForeignKey(Folder, verbose_name="Папка", on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField("Название", max_length=255)
    audio = models.FileField("Аудио", upload_to="contents/%Y/%m/%d")
    status = models.CharField("Статус", max_length=32, choices=StatusChoices.choices, default="QUEUE")
    duration = models.PositiveIntegerField("Длительность", blank=True, null=True)
    original_language = models.CharField("Оригинальный язык", max_length=32)
    translate_to = models.CharField("Перевод на", max_length=32)
    additional_data = models.JSONField("Дополнительные данные", default=dict, blank=True, null=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контенты"


class Speech(models.Model):
    content = models.ForeignKey(Content, verbose_name="Контент", on_delete=models.CASCADE, related_name="speeches")
    speaker = models.CharField("Говорящий", max_length=32)
    from_time = models.DecimalField("Время начала", max_digits=6, decimal_places=2)
    to_time = models.DecimalField("Время конца", max_digits=6, decimal_places=2)
    text = models.TextField("Текст")

    class Meta:
        verbose_name = "Речь"
        verbose_name_plural = "Речи"
