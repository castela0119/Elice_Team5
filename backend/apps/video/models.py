from gc import DEBUG_COLLECTABLE
from imp import source_from_cache
from django.db import models
from backend.apps.user_app.models import MyUser

# Create your models here.
class Video(models.Model):
    """
    Video 모델
    """

    user_id = models.ForeignKey(
        MyUser,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="video_user",
        null=True,
        blank=True,
        default="",
    )

    source = models.URLField(
        verbose_name="동영상 URL",
    )

    title = models.CharField(
        verbose_name="동영상 제목",
        max_length=255,
        blank=True,
        default="",
    )

    thumbnail = models.URLField(
        verbose_name="썸네일 URL",
        blank=True,
        default="",
    )

    author = models.CharField(
        verbose_name="업로드 한 사람",
        max_length=255,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name_plural = "비디오"
        db_table = "video"

    def __str__(self):
        return self.title


class Keyword(models.Model):
    """
    Keyword 모델
    """

    video = models.ForeignKey(
        Video,
        verbose_name="동영상 id",
        on_delete=models.CASCADE,
        related_name="time_keywords",
    )

    timestamp = models.TimeField(
        verbose_name="타임스탬프",
        blank=True,
        default="",
    )

    keyword = models.CharField(
        verbose_name="시간대 키워드",
        max_length=255,
        blank=True,
        default="",
    )

    score = models.FloatField(
        verbose_name="키워드 점수",
        blank=True,
        default=0,
    )

    class Meta:
        verbose_name_plural = "키워드"
        db_table = "keyword"

    def __str__(self):
        return self.keyword


class Frequency(models.Model):
    """
    Frequency 모델
    """

    video = models.ForeignKey(
        Video,
        verbose_name="동영상 id",
        on_delete=models.CASCADE,
        related_name="keywords_frequency",
    )

    keyword = models.CharField(
        verbose_name="키워드",
        max_length=255,
    )

    count = models.IntegerField(
        verbose_name="키워드 빈도 수",
        default=0,
    )

    class Meta:
        verbose_name_plural = "키워드 빈도 수"
        db_table = "frequency"

    def __str__(self):
        return self.keyword
