import os
import datetime
import time
import subprocess
import whisper
from pydub import AudioSegment
from pyannote.audio import Pipeline
from django.conf import settings
from celery import shared_task

# from config.celery import PYANNOTATE_PIPELINE, WHISPER_MODEL
from storage import models
from ml.pyannote import transcription, translation, utils


@shared_task
def run(content_pk):
    print("start")
    try:
        content = models.Content.objects.get(pk=content_pk)
        today = datetime.datetime.today()
        year, month, day = today.year, today.month, today.day
        audio_path = f"{settings.MEDIA_ROOT}/original_audio/{year}/{month}/{day}"
        os.makedirs(f"{settings.MEDIA_ROOT}/original_audio/{year}/{month}/{day}", exist_ok=True)
        audio_path = f"{audio_path}/{content.original_video.name.split('/')[-1].replace('.mp4', '')}.wav"
        command = f"ffmpeg -y -i {content.original_video.path} -acodec pcm_s16le -ac 1 -ar 16000 {audio_path}"
        subprocess.call(command)
        audio_segment = AudioSegment.from_wav(audio_path)
        print("PRE SAVE")
        content.original_audio = audio_path
        content.save()
        print("CONTENT SAVED")

        start_time = time.time()
        pipeline = Pipeline.from_pretrained(
            checkpoint_path="pyannote/speaker-diarization-3.1", use_auth_token=settings.PYANNOTE_AUTH_TOKEN
        )
        print("pipeline loaded", time.time() - start_time)

        start_time = time.time()
        model = whisper.load_model("medium")
        print("whisper loaded", time.time() - start_time)

        start_time = time.time()
        diarization_res = pipeline(audio_path, num_speakers=content.additional_data.get("num_speakers", None))
        print("pipeline executed", time.time() - start_time)

        start_time = time.time()
        transcribe_res = model.transcribe(audio_path, word_timestamps=True)
        print("whisper executed", time.time() - start_time)

        start_time = time.time()
        result = transcription.diarize_text(transcribe_res, diarization_res)
        print("final result done", time.time() - start_time)
        print("asr res", transcribe_res["segments"])
        # ------------------------------------------------------------
        translated_list = translation.get_translated_text(result, content.translate_to)
        utils.create_speeches(content.pk, result, translated_list)
        #
        speeches = models.Speech.objects.filter(content_id=content.pk)
        speakers = list(speeches.distinct("speaker").values_list("speaker", flat=True))

        # TODO
        # for speaker in speakers:
        #     path = f"{os.getcwd()}/{speaker}"
        #     os.mkdir(path)
        #     for speech in speeches.filter(speaker=speaker).order_by("from_time"):
        #         from_time, to_time = int(speech.from_time * 1000), int(speech.to_time * 1000)
        #         cut_audio = audio_segment[from_time:to_time]
        #         cut_audio.export(f"{os.getcwd()}/{speaker}/{from_time // 10}_{to_time // 10}.wav", format="wav")

        # TODO call TTS
        content.duration = utils.get_audio_duration(audio_path)
        content.status = models.Content.StatusChoices.processed
        content.save()
    except Exception as e:
        print("Exception", e)
        models.Content.objects.filter(pk=content_pk).update(status=models.Content.StatusChoices.failed)
