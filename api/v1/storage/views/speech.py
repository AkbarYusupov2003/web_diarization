from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from api.v1.storage import serializers
from api.v1.storage import utils
from storage import models


class SpeechCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.SpeechSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"kwargs": self.kwargs})
        return context

    def create(self, request, *args, **kwargs):
        get_object_or_404(models.Content, pk=kwargs["content_pk"], owner_id=request._auth.payload["user_id"])
        request.data["content"] = kwargs["content_pk"]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        utils.create_file_for_speech(serializer.instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SpeechDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.SpeechSerializer
    http_method_names = ("get", "patch", "delete")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"kwargs": self.kwargs})
        return context

    def get_object(self):
        content = get_object_or_404(
            models.Content, pk=self.kwargs["content_pk"], owner_id=self.request._auth.payload["user_id"]
        )

        return get_object_or_404(models.Speech, pk=self.kwargs["speech_pk"], content=content)
