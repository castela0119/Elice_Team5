from backend.apps.script.serializers import ScriptSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Frequency, Keyword, Video


class VideoIdSerializer(ModelSerializer):

    video_id = serializers.SerializerMethodField()

    def get_video_id(self, obj):
        return obj.id

    class Meta:
        model = Video
        fields = ("video_id",)


class KeywordSerializer(ModelSerializer):
    class Meta:
        model = Keyword
        exclude = ("video", "id")


class FrequencySerializer(ModelSerializer):
    class Meta:
        model = Frequency
        exclude = ("video", "id")


class VideoSerializer(ModelSerializer):

    time_keywords = KeywordSerializer(many=True, read_only=True)
    time_scripts = ScriptSerializer(many=True, read_only=True)
    keywords_frequency = FrequencySerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = (
            "id",
            "user_id",
            "source",
            "youtube_slug",
            "title",
            "thumbnail",
            "author",
            "time_scripts",
            "keywords_frequency",
            "time_keywords",
        )

    def create(self, validated_data):
        return Video.objects.create(**validated_data)
