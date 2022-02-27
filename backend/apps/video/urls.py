from django.urls import path
from .views import VideoListAPIView, VideoAPIView, KeywordAPIView, FrequencyAPIView, VideoSlugAPIView

urlpatterns = [
    path('list/', VideoListAPIView.as_view(), name='videolist'),
    path('', VideoAPIView.as_view()),
    path('<int:video_id>/', VideoAPIView.as_view(), name='video_detail'),
    path('<int:video_id>/keywords/', KeywordAPIView.as_view(), name='video_keywords'),
    path('<int:video_id>/frequencies/', FrequencyAPIView.as_view(), name='video_frequencies'),
    path('<int:video_id>/slug/', VideoSlugAPIView.as_view(), name='video_slug'),
]