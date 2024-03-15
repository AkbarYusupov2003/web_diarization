from rest_framework import serializers

from storage import models


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Content
        fields = ("pk", "owner", "title",  "audio", "language", "duration", "additional_data")


class SpeechSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Speech
        fields = ("pk", "content", "speaker", "from_time", "to_time", "text")
