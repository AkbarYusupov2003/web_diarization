from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from api.v1.storage import serializers
from storage import models


class FolderListAPIView(generics.ListAPIView):
    serializer_class = serializers.FolderSerializer

    def get_queryset(self):
        queryset = models.Folder.objects.filter(owner_id=self.request._auth.payload["user_id"])
        search = str(self.request.data.get("search", ""))
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset


class FolderCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.FolderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FolderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Folder
    serializer_class = serializers.FolderSerializer
    http_method_names = ("get", "patch", "delete")

    def get_object(self):
        return get_object_or_404(self.queryset, owner_id=self.request._auth.payload["user_id"], pk=self.kwargs["pk"])
