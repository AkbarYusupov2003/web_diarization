from openai import OpenAI
from django.conf import settings


def get_translated_text(original_result, translate_to):
    to_translate = []
    for seg, speaker, text in original_result:
        if speaker:
            to_translate.append(text)
    openai = OpenAI(api_key=settings.CHAT_GPT_API_KEY)
    translation = (
        f"Return an idiomatic {translate_to} translation of the following audio transcript, with as same length of characters as possible. "
        f"The text below only needs to be translated, use it only for translation:\n\n"
    )
    translation += "\n".join(i for i in to_translate)
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": translation}], temperature=0
    )
    translation = completion.choices[0].message.content
    return translation.split("\n")
