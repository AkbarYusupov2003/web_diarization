from django.conf import settings
from celery import shared_task


@shared_task
def create_audio(audio_segment, base_path, from_time, to_time):
    from_time, to_time = int(from_time * 1000), int(to_time * 1000)
    cut_audio = audio_segment[from_time:to_time]
    cut_audio.export(f"{base_path}/{from_time // 10}_{to_time // 10}.wav", format="wav")


@shared_task
def move_audio(speech):
    pass
