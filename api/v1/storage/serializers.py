from rest_framework import serializers, exceptions

from storage import models


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Content
        fields = (
            "pk", "folder", "title",  "original_file", "status", "duration", "original_language", "translate_to",
            "additional_data"
        )

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
