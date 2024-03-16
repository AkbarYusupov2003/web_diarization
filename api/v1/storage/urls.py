from django.urls import path

from api.v1.storage import views


urlpatterns = [
    # Content
    path("content/list/", views.ContentListAPIView.as_view()),
    path("content/create/", views.ContentCreateAPIView.as_view()),
    path("content/<int:pk>/", views.ContentDetailAPIView.as_view()),
    # Speech
    path("content/<int:content_pk>/speech/create/", views.SpeechCreateAPIView.as_view()),
    path("content/<int:content_pk>/speech/<int:speech_pk>/", views.SpeechDetailAPIView.as_view()),
]
