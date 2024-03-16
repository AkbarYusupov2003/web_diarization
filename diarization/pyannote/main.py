import time

import whisper
from openai import OpenAI
from pyannote.audio import Pipeline
from django.conf import settings
from celery import shared_task

# from config.celery import PYANNOTATE_PIPELINE, WHISPER_MODEL
from storage import models
from diarization.pyannote.whisper.utils import diarize_text


@shared_task
def run(pk):
    print("start")
    content = models.Content.objects.get(pk=pk)
    audio = content.audio.path
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
        final_result = diarize_text(transcribe_res, diarization_res)
        print("final result done", time.time() - start_time)

        # print("asr res", transcribe_res["segments"])

        to_create = []

        # for translation only
        to_translate = []
        for seg, speaker, text in final_result:
            if speaker:
                to_translate.append(text)
        openai = OpenAI(api_key=settings.CHAT_GPT_API_KEY)
        to_lang = "Russian"
        translation = f"Return an idiomatic {to_lang} translation of the following audio transcript, the text below only needs to be translated, use it only for translation:\n\n"
        translation += "\n".join(i for i in to_translate)
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": translation}], temperature=0
        )
        translation = completion.choices[0].message.content
        translated = translation.split("\n")
        # ended
        i = 0

        for seg, speaker, text in final_result:
            if speaker:
                to_create.append(
                    models.Speech(
                        content_id=content.pk,
                        speaker=speaker,
                        from_time=f"{seg.start:.2f}",
                        to_time=f"{seg.end:.2f}",
                        text=f"{text} ||| "#{translated[i]}"
                    )
                )
                i += 1
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
