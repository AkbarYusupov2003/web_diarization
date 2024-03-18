from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

import ml
from api.v1.storage import serializers
from storage import models


class ContentListAPIView(generics.ListAPIView):
    serializer_class = serializers.ContentSerializer

    def get_queryset(self):
        queryset = models.Content.objects.filter(owner_id=self.request._auth.payload["user_id"])
        search = str(self.request.data.get("search", ""))
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset


class ContentCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.ContentSerializer

    def create(self, request, *args, **kwargs):
        # TODO validate folder

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # ml.run_pyannote(serializer.instance.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ContentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Content
    serializer_class = serializers.ContentSerializer
    http_method_names = ("get", "patch", "delete")

    def get_object(self):
        return get_object_or_404(self.queryset, owner_id=self.request._auth.payload["user_id"], pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(models.Content, owner_id=request._auth.payload["user_id"], pk=self.kwargs["pk"])
        content = serializers.ContentSerializer(instance).data
        content["speeches"] = serializers.SpeechSerializer(instance.speeches.all(), many=True).data
        return Response(content, status=status.HTTP_200_OK)
