from django.contrib.auth import get_user_model
from django.db import models


class Content(models.Model):
    class StatusChoices(models.TextChoices):
        # in queue, diarizing, transcribing, translating
        processing = "PROCESSING", "Обрабатывается"
        processed = "PROCESSED", "Обработан"
        failed = "FAILED", "Ошибка"

    owner = models.ForeignKey(
        get_user_model(), verbose_name="Владелец", on_delete=models.CASCADE, related_name="contents"
    )
    title = models.CharField("Название", max_length=255)
    audio = models.FileField("Аудио", upload_to="contents/%Y/%m/%d")
    status = models.CharField("Статус", max_length=32, choices=StatusChoices.choices, default="PROCESSING")
    duration = models.DecimalField(
        "Длительность", max_digits=8, decimal_places=2, blank=True, null=True
    )
    language = models.CharField("Язык аудио", default="en", max_length=8)
    additional_data = models.JSONField("Дополнительные данные", default=dict, blank=True, null=True)

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
