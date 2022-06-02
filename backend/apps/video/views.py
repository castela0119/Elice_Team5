import typing as ty

from backend.apps.ai.page_rank import YoutubeInference
from backend.apps.script.models import Script
from backend.apps.video.models import Frequency, Keyword, Video
from backend.apps.video.serializers import VideoIdSerializer, VideoSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView


class VideoListAPIView(APIView):
    """
    로그인 한 유저의  관련 REST API 제공
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="유저 페이지에 저장된 영상 리스트",
        responses={
            200: VideoSerializer(many=True),
            401: "자격 인증 데이터가 제공되지 않았습니다.",
            500: "SERVER ERROR",
        },
    )
    def get(self, request):
        """
        로그인 한 유저가 분석한 Video list 불러오는 API
        """
        user = self.request.user
        videos = Video.objects.filter(user_id=user)
        serializer = VideoSerializer(videos, many=True)

        return Response(serializer.data)


class VideoDetailAPIView(APIView):
    """
    상세 비디오 관련 REST API 제공
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="특정 영상 상세 정보",
        responses={
            200: VideoSerializer(),
            404: "ERROR: Video not found",
            500: "SERVER ERROR",
        },
    )
    def get(self, request, video_id):
        """
        video_id에 해당하는 특정 비디오를 불러오는 API
        """
        try:
            video = Video.objects.filter(id=video_id).first()
            serializer = VideoSerializer(video)
            return Response(serializer.data)

        except Video.DoesNotExist:
            return Response(
                {"error": "Video Not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_summary="영상 마이 페이지에 저장 요청",
        operation_description="video_id에 해당하는 특정 비디오를 유저 페이지에 저장하는 API",
        responses={
            200: "성공적으로 저장되었습니다.",
            404: "해당 id에 해당하는 video가 없습니다.",
            500: "SERVER ERROR",
        },
    )
    def post(self, request, video_id):
        """
        video_id에 해당하는 특정 비디오를 유저 페이지에 저장하는 API
        """
        try:
            video = Video.objects.filter(id=video_id).first()
            video.user_id = self.request.user
            video.save()
            return Response({"detail": "성공적으로 저장되었습니다."})

        except Exception:
            return Response(
                {"error": "해당 id에 해당하는 video가 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_summary="영상 마이 페이지에서 삭제 요청",
        operation_description="video_id에 해당하는 특정 비디오를 유저 페이지에서 삭제하는 API",
        responses={
            200: "성공적으로 삭제되었습니다.",
            404: "해당 id에 해당하는 video가 없습니다.",
            500: "SERVER ERROR",
        },
    )
    def delete(self, request, video_id):
        """
        video_id에 해당하는 특정 비디오를 유저 페이지에서 삭제하는 API
        """
        try:
            video = Video.objects.filter(id=video_id).first()
            video.user_id = None
            video.save()
            return Response({"detail": "성공적으로 삭제되었습니다."})

        except Exception:
            return Response(
                {"error": "해당 id에 해당하는 video가 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )


class VideoAPIView(APIView):
    """
    Video 관련 REST API 제공
    """

    youtube_url_prefix = "https://www.youtube.com/watch?v="

    def store_keywords_info(self, keywords_info, video):
        for idx in keywords_info:
            keyword = Keyword(video=video)
            keyword.timestamp = keywords_info[idx]["timestamp"]
            keyword.keyword = keywords_info[idx]["keyword"]
            keyword.score = keywords_info[idx]["score"]
            keyword.save()

    def store_scripts_info(self, scripts_info, video):
        for timestamp in scripts_info:
            script = Script(video=video)
            script.timestamp = timestamp
            script.content = scripts_info[timestamp]["script"]
            script.importance_score = scripts_info[timestamp]["importance"]
            script.save()

    def store_frequency(self, words_freq, video):
        for word in words_freq:
            frequency = Frequency(video=video)
            frequency.keyword = word
            frequency.count = words_freq[word]
            frequency.save()

    @swagger_auto_schema(
        operation_summary="영상 분석 요청",
        responses={
            200: VideoIdSerializer(),
            400: "ERROR: Unsupported video.",
            500: "SERVER ERROR",
        },
        request_body=serializers.Serializer(),
    )
    def post(self, request):
        """
        특정 Video url을 AI 모델에 전달하여 분석한 결과를 DB에 저장하고 결과 리턴하는 API

        ---
        ### 요청 바디에 {'youtube_slug': '비디오 식별자'} 형식으로 보내면 됩니다!
        """
        request.data["source"] = self.youtube_url_prefix + request.data.get(
            "youtube_slug"
        )
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        source = validated_data.get("source")
        youtube_slug = validated_data.get("youtube_slug")

        # url로 중요도 분석
        youtube_inference = YoutubeInference(source)

        video = Video(source=source, youtube_slug=youtube_slug)
        video.author = youtube_inference.author
        video.title = youtube_inference.title
        video.thumbnail = youtube_inference.thumbnail_url
        video.save()

        # scripts, keywords, frequency 저장
        inference_result: ty.List[dict] = youtube_inference.inference()
        if len(inference_result) != 3:
            return Response(
                {"error": "Unsupported video."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        scripts_info, keywords_info, words_freq = inference_result

        self.store_keywords_info(keywords_info, video)
        self.store_scripts_info(scripts_info, video)
        self.store_frequency(words_freq, video)

        serializer = VideoIdSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
