from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

import diarization
from api.v1.storage import serializers
from storage import models


# Content
class ContentListAPIView(generics.ListAPIView):
    serializer_class = serializers.ContentSerializer

    def get_queryset(self):
        return models.Content.objects.filter(owner_id=self.request._auth.payload["user_id"])


class ContentCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.ContentSerializer

    def create(self, request, *args, **kwargs):
        request.data["owner"] = request._auth.payload["user_id"]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = serializer.instance
        diarization.run_pyannote(instance.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ContentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Content
    serializer_class = serializers.ContentSerializer
    http_method_names = ("get", "patch", "delete")

    def get_object(self):
        return get_object_or_404(self.queryset, owner_id=self.request._auth.payload["user_id"], pk=self.kwargs["pk"])

    # TODO IN PATCH IF AUDIO FILE CHANGED -> DELETE SPEECHES -> DIARIZE
    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(models.Content, owner_id=request._auth.payload["user_id"], pk=self.kwargs["pk"])
        content = serializers.ContentSerializer(instance).data
        content["speeches"] = serializers.SpeechSerializer(instance.speeches.all(), many=True).data
        return Response(content, status=status.HTTP_200_OK)


# Speech
class SpeechCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.SpeechSerializer

    def create(self, request, *args, **kwargs):
        get_object_or_404(models.Content, pk=kwargs["content_pk"], owner_id=request._auth.payload["user_id"])
        request.data["content"] = kwargs["content_pk"]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SpeechDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.SpeechSerializer
    http_method_names = ("get", "patch", "delete")

    def get_object(self):
        content = get_object_or_404(
            models.Content, pk=self.kwargs["content_pk"], owner_id=self.request._auth.payload["user_id"]
        )
        return get_object_or_404(models.Speech, pk=self.kwargs["speech_pk"], content=content)
