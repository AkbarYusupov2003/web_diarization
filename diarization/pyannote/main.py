import whisper
import wave
from pyannote.audio import Pipeline
from django.conf import settings
from celery import shared_task

# from config.celery import PYANNOTATE_PIPELINE, WHISPER_MODEL
from storage import models
from diarization.pyannote.whisper.utils import diarize_text


@shared_task
def run(pk):
    content = models.Content.objects.get(pk=pk)
    audio = content.audio.path
    try:
        # diarization = PYANNOTATE_PIPELINE(content.audio.path)
        # for turn, _, speaker in diarization.itertracks(yield_label=True):
        #    print(f"{speaker} start={turn.start:.1f}s stop={turn.end:.1f}s ")
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1", use_auth_token=settings.PYANNOTE_AUTH_TOKEN
        )
        model = whisper.load_model("medium")
        # if content.language == "ru":
        #     model = whisper.load_model("medium.ru")
        # elif content.language == "en":
        #     model = whisper.load_model("medium.en")
        # else:
        #     model = whisper.load_model("medium")
        asr_result = model.transcribe(audio, suppress_silence=True, ts_num=16, lower_quantile=0.05, lower_threshold=0.1)
        # max_initial_timestamp=None
        diarization_result = pipeline(audio)
        print("asr res", asr_result["segments"])
        final_result = diarize_text(asr_result, diarization_result)
        to_create = []
        for seg, speaker, text in final_result:
            if speaker:
                to_create.append(
                    models.Speech(
                        content_id=content.pk,
                        speaker=speaker,
                        from_time=f"{seg.start:.2f}",
                        to_time=f"{seg.end:.2f}",
                        text=text
                    )
                )
        models.Speech.objects.bulk_create(to_create)
        # with wave.open(audio) as f:
        #     seconds = f.getnframes() / f.getframerate()
        #     content.duration = f"{seconds:.2f}"
        content.status = models.Content.StatusChoices.processed
        content.save()
    except Exception as e:
        print("Exception", e)
        content.status = models.Content.StatusChoices.failed
        content.save()
