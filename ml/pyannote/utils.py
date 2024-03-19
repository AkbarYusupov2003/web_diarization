import wave
from storage import models


def create_speeches(content_id, result, translated_text):
    to_create = []
    i = 0
    for seg, speaker, text in result:
        if speaker:
            to_create.append(
                models.Speech(
                    content_id=content_id,
                    speaker=speaker,
                    from_time=f"{seg.start:.2f}",
                    to_time=f"{seg.end:.2f}",
                    text=f"{text} ||| {translated_text[i]}"
                )
            )
            i += 1
    models.Speech.objects.bulk_create(to_create)


def get_audio_duration(audio_path):
    with wave.open(audio_path) as f:
        seconds = f.getnframes() / f.getframerate()
    return int(seconds)
