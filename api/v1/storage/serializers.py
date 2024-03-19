import os
from django.conf import settings
from pydub import AudioSegment
from rest_framework import serializers, exceptions

from api.v1.utils import speech_file
from storage import models


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Content
        fields = (
            "pk", "folder", "title",  "original_video", "status", "duration", "original_language", "translate_to",
            "additional_data"
        )

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields["original_video"].read_only = True
        return fields

    def create(self, validated_data):
        validated_data["owner_id"] = self.context.get("request")._auth.payload["user_id"]
        return super().create(validated_data)

    def validate_folder(self, value):
        if value:
            if value.owner_id == self.context.get("request")._auth.payload["user_id"]:
                return value
            else:
                raise exceptions.ValidationError("folder validation error")
        else:
            return None


class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Folder
        fields = ("pk", "title")

    def create(self, validated_data):
        validated_data["owner_id"] = self.context.get("request")._auth.payload["user_id"]
        return super().create(validated_data)


class SpeechSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Speech
        fields = ("pk", "content", "speaker", "from_time", "to_time", "text")

    def create(self, validated_data):
        validated_data["content_id"] = self.context.get("kwargs")["content_pk"]
        return super().create(validated_data)

    def update(self, instance, validated_data):
        print("validated_data", validated_data)
        if instance.speaker != validated_data.get("speaker", instance.speaker):
            print("CHANGED")
            base = f"{settings.AUDIOS_URL}/content_{instance.content_id}"
            dst = f"{base}/{validated_data['speaker']}"
            audio_name = f"{int(instance.from_time * 100)}_{int(instance.to_time * 100)}.wav"
            if not os.path.exists(dst):
                os.mkdir(dst)

            if instance.from_time == validated_data.get("from_time", instance.from_time) and \
               instance.to_time == validated_data.get("to_time", instance.to_time):
                os.rename(src=f"{base}/{instance.speaker}/{audio_name}", dst=f"{dst}/{audio_name}")
            else:
                # DELETE EXISTING AUDIO AND CREATE NEW
                os.remove(f"{base}/{instance.speaker}/{audio_name}")

                audio_segment = AudioSegment.from_wav(instance.content)
                # cut_audio =

                # for speaker in speakers:
                #     path = f"{os.getcwd()}/{speaker}"
                #     os.mkdir(path)
                #     for speech in speeches.filter(speaker=speaker).order_by("from_time"):
                #         from_time, to_time = int(speech.from_time * 1000), int(speech.to_time * 1000)
                #         cut_audio = audio_segment[from_time:to_time]
                #         cut_audio.export(f"{os.getcwd()}/{speaker}/{from_time // 10}_{to_time // 10}.wav", format="wav")



        elif instance.from_time == validated_data.get("from_time", instance.from_time) and \
             instance.to_time == validated_data.get("to_time", instance.to_time):
            print("NOT CHANGED")


        return super().update(instance, validated_data)
