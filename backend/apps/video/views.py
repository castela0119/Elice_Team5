from .models import Video, Keyword, Frequency
from .serializers import VideoSerializer, VideoIdSerializer, VideoSlugSerializer
from rest_framework import status, serializers
from rest_framework.views import APIView
from .models import Video
from backend.apps.script.models import Script
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend.apps.ai.page_rank import YoutubeInference
from drf_yasg.utils import swagger_auto_schema


class VideoSlugAPIView(APIView):
    """
    Video Slug 관련 REST API 제공
    """

    @swagger_auto_schema(
        operation_summary="영상 식별자",
        responses={
            200: VideoSlugSerializer(),
            404: 'ERROR: Video or Video slug Not found',
            500: 'SERVER ERROR'
        }
    )
    def get(self, request, video_id):
        """
        Video Slug 불러오는 API
        """
        try:
            video = Video.objects.filter(id=video_id).first()
            serializer = VideoSlugSerializer(video)
            
            return Response(serializer.data)
        except:
            return Response({'error': 'Video or Video slug Not found'}, status=status.HTTP_404_NOT_FOUND)


class VideoListAPIView(APIView):
    """
    로그인 한 유저의  관련 REST API 제공
    """
    permission_classes = [IsAuthenticated]

    def get_user(self):
        return self.request.user

    @swagger_auto_schema(
        operation_summary="유저 페이지에 저장된 영상 리스트",
        responses={
            200: VideoSerializer(many=True),
            401: '자격 인증 데이터가 제공되지 않았습니다.',
            500: 'SERVER ERROR'
        }
    )
    def get(self, request):
        """
        로그인 한 유저가 분석한 Video list 불러오는 API 
        """
        user = self.get_user()
        videos = Video.objects.filter(user_id=user)
        serializer = VideoSerializer(videos, many=True)
        
        return Response(serializer.data)


class VideoDetailAPIView(APIView):
    """
    상세 비디오 관련 REST API 제공
    """
    # TODO:is owner로 바꿔야 할것같다.
    permission_classes = [IsAuthenticated]

    def get_user(self):
        return self.request.user

    @swagger_auto_schema(
        operation_summary="특정 영상 상세 정보",
        responses={
            200: VideoSerializer(),
            404: 'ERROR: Video not found',
            500: 'SERVER ERROR'
        }
    )
    def get(self, request, video_id):
        """
        video_id에 해당하는 특정 비디오를 불러오는 API
        """
        try:
            video = Video.objects.filter(pk=video_id).first()
            serializer = VideoSerializer(video)
            return Response(serializer.data)

        except Video.DoesNotExist:
            return Response({'error': 'Video Not found'}, status=status.HTTP_404_NOT_FOUND)


    @swagger_auto_schema(
        operation_summary="영상 마이 페이지에 저장 요청",
        operation_description="video_id에 해당하는 특정 비디오를 유저 페이지에 저장하는 API",
        responses={
            200: '성공적으로 저장되었습니다.',
            404: '해당 id에 해당하는 video가 없습니다.',
            500: 'SERVER ERROR'
        },
    )
    def post(self, request, video_id):
        """
        video_id에 해당하는 특정 비디오를 유저 페이지에 저장하는 API
        """
        try:
            video = Video.objects.filter(pk=video_id).first()
            video.user_id = self.get_user()
            video.save()
            return Response({'detail': '성공적으로 저장되었습니다.'})

        except:
            return Response({'error': '해당 id에 해당하는 video가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


    @swagger_auto_schema(
        operation_summary="영상 마이 페이지에서 삭제 요청",
        operation_description="video_id에 해당하는 특정 비디오를 유저 페이지에서 삭제하는 API",
        responses={
            200: '성공적으로 삭제되었습니다.',
            404: '해당 id에 해당하는 video가 없습니다.',
            500: 'SERVER ERROR'
        },
    )
    def delete(self, request, video_id):
        """
        video_id에 해당하는 특정 비디오를 유저 페이지에서 삭제하는 API
        """
        try:
            video = Video.objects.filter(pk=video_id).first()
            video.user_id = None
            video.save()
            return Response({'detail': '성공적으로 삭제되었습니다.'})

        except:
            return Response({'error': '해당 id에 해당하는 video가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)



class VideoAPIView(APIView):
    """
    Video 관련 REST API 제공
    """
    youtube_url_prefix = "https://www.youtube.com/watch?v="

    def store_keywords_info(self, keywords_info, video):
        for idx in keywords_info:
            keyword = Keyword(video=video)
            keyword.timestamp = keywords_info[idx]['timestamp']
            keyword.keyword = keywords_info[idx]['keyword']
            keyword.score = keywords_info[idx]['score']
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
            400: 'ERROR: Unsupported video url. Please check the video is on youtube and support korean script.',
            500: 'SERVER ERROR'
        },
        request_body=serializers.Serializer(),
    )
    def post(self, request):
        """
        특정 Video url을 AI 모델에 전달하여 분석한 결과를 DB에 저장하고 결과 리턴하는 API
        
        ---
        ### 요청 바디에 {'source': '비디오 식별자'} 형식으로 보내면 됩니다! 
        """
        request.data["source"] = self.youtube_url_prefix + request.data.get("source")
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        source = validated_data.get("source")

        # url로 중요도 분석
        youtube_inference = YoutubeInference(source)
        
        video = Video(source = source)
        video.author = youtube_inference.author
        video.title = youtube_inference.title
        video.thumbnail = youtube_inference.thumbnail_url
        video.save()

        # scripts, keywords, frequency 저장
        inf_result = youtube_inference.inference()
        if inf_result:
            scripts_info, keywords_info, words_freq = inf_result
            
            self.store_keywords_info(keywords_info, video)
            self.store_scripts_info(scripts_info, video)
            self.store_frequency(words_freq, video)

            serializer = VideoIdSerializer(video)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"error": "Unsupported video url. Please check the video is on youtube and support korean script."}, status=status.HTTP_400_BAD_REQUEST)