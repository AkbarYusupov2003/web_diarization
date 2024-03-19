from django.conf import settings
from celery import shared_task


@shared_task
def create_file(speech):
    print(settings.AUDIOS_URL)


@shared_task
def move_file(speech):
    pass
