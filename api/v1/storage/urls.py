from django.urls import path

from api.v1.storage import views


urlpatterns = [
    # Content
    path("content/list/", views.ContentListAPIView.as_view()),
    path("content/create/", views.ContentCreateAPIView.as_view()),
    path("content/<int:pk>/", views.ContentDetailAPIView.as_view()),
    # Speech
    path("speech/create/<int:content_pk>/", views.SpeechCreateAPIView.as_view()),
    path("speech/detail/<int:content_pk>/<int:speech_pk>/", views.SpeechDetailAPIView.as_view()),
]
