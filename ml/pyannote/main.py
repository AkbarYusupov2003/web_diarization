import os
import time
import subprocess
import whisper
from pyannote.audio import Pipeline
from django.conf import settings
from celery import shared_task

# from config.celery import PYANNOTATE_PIPELINE, WHISPER_MODEL
from storage import models
from ml.pyannote import transcription, translation, utils


@shared_task
def run(pk):
    print("start")
    content = models.Content.objects.get(pk=pk)

    print(os.path.splitext(content.original_file.name)[1])
    print(content.original_file.path)
    p = "C:\\Users\\le.mp4"
    # os get current path and set
    if os.path.splitext(content.original_file.name)[1] == ".mp4":
        p = "C:\\Users\\le.mp4"
        command = f"ffmpeg -i {p} -acodec pcm_s16le -ac 1 -ar 16000 audio.wav"
        # ffmpeg -i input.mp3 -acodec pcm_s16le -ac 1 -ar 16000 output.wav
        subprocess.call(command, shell=True)

    return "stop"
    audio = content.original_file.path
    try:
        start_time = time.time()
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1", use_auth_token=settings.PYANNOTE_AUTH_TOKEN
        )
        print("pipeline loaded", time.time() - start_time)

        start_time = time.time()
        model = whisper.load_model("medium")
        print("whisper loaded", time.time() - start_time)

        start_time = time.time()
        diarization_res = pipeline(audio)
        print("pipeline executed", time.time() - start_time)

        start_time = time.time()
        transcribe_res = model.transcribe(audio, word_timestamps=True)
        print("whisper executed", time.time() - start_time)

        start_time = time.time()
        result = transcription.diarize_text(transcribe_res, diarization_res)
        print("final result done", time.time() - start_time)
        print("asr res", transcribe_res["segments"])
        # ------------------------------------------------------------
        translated_list = translation.get_translated_text(result, content.translate_to)
        utils.create_speeches(content.pk, result, translated_list)
        #
        content.duration = utils.get_audio_duration(audio)
        content.status = models.Content.StatusChoices.processed
        content.save()
    except Exception as e:
        print("Exception", e)
        content.status = models.Content.StatusChoices.failed
        content.save()
