from django.urls import path

from .views import VideoAPIView, VideoDetailAPIView, VideoListAPIView

urlpatterns = [
    path("list/", VideoListAPIView.as_view(), name="videolist"),
    path("", VideoAPIView.as_view(), name="video_post"),
    path("<str:video_id>/", VideoDetailAPIView.as_view(), name="video_detail_info"),
]
