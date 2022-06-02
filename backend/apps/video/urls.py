from django.urls import path
from .views import VideoListAPIView, VideoAPIView, VideoDetailAPIView, VideoSlugAPIView

urlpatterns = [
    path('list/', VideoListAPIView.as_view(), name='videolist'),
    path('', VideoAPIView.as_view(), name='video_post'),
    path('<int:video_id>/', VideoDetailAPIView.as_view(), name='video_detail_info'),
    path('<int:video_id>/slug/', VideoSlugAPIView.as_view(), name='video_slug'),
]