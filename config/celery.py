import os

import whisper
from celery import Celery
from django.conf import settings
# from pyannote.audio import Pipeline


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.core")

app = Celery("config")
app.config_from_object(settings, namespace="CELERY")

# PYANNOTATE_PIPELINE = Pipeline.from_pretrained(
#     checkpoint_path="pyannote/speaker-diarization-3.1", use_auth_token=settings.PYANNOTE_AUTH_TOKEN
# )
# WHISPER_MODEL = whisper.load_model("medium")

app.autodiscover_tasks()
