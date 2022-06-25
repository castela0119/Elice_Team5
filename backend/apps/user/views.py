from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import (
    TokenBlacklistSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .serializers import MyTokenObtainPairSerializer, RegistrationSerializer


class RegisterView(APIView):
    """
    유저 회원가입을 위한 REST API
    """

    @swagger_auto_schema(
        operation_summary="회원가입",
        request_body=RegistrationSerializer,
        tags=["user"],
        operation_description="회원가입",
        responses={201: "회원가입 성공", 401: "없는 회원이거나 비밀번호 틀림"},  # can use schema or text
    )
    def post(self, request, *args, **kwargs):
        """
        회원가입 요청 API
        """
        if request.method == "POST":
            serializer = RegistrationSerializer(data=request.data)

            data = {}

            if serializer.is_valid():
                user = serializer.save()

                data["response"] = "Registration Successful!"
                data["user_ID"] = user.user_ID
                data["email"] = user.email

                return Response(data, status=status.HTTP_201_CREATED)

            else:
                data = serializer.errors
                return Response(data, status=status.HTTP_409_CONFLICT)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_summary="로그인 시 토큰 발급",
        request_body=MyTokenObtainPairSerializer,
        tags=["user"],
        operation_description="로그인 시 토큰 발급",
        responses={200: "로그인 성공", 409: "없는 회원이거나 비밀번호 틀림"},  # can use schema or text
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)

        except Exception:
            return Response("not user or wrong password!", status.HTTP_409_CONFLICT)


class MyTokenVerifyView(TokenVerifyView):
    serializer_class = TokenVerifySerializer

    @swagger_auto_schema(
        operation_summary="토큰 유효 확인",
        request_body=TokenVerifySerializer,
        tags=["user"],
        operation_description="토큰 유효 확인",
        responses={200: "토큰 유효", 401: "토큰 무효"},  # can use schema or text
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)

        except Exception:
            return Response("Token is invalid or expired", status.HTTP_401_UNAUTHORIZED)


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(
        operation_summary="토큰 재발행",
        request_body=TokenRefreshSerializer,
        tags=["user"],
        operation_description="토큰 재발행",
        responses={200: "토큰 재발행 성공", 401: "없는 토큰"},  # can use schema or text
    )
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class MyTokenBlacklistView(TokenBlacklistView):
    serializer_class = TokenBlacklistSerializer

    @swagger_auto_schema(
        operation_summary="토큰 블랙리스트",
        request_body=TokenBlacklistSerializer,
        tags=["user"],
        operation_description="토큰 블랙리스트",
        responses={  # can use schema or text
            200: "로그아웃 성공",
            401: "이미 로그아웃 됨(토큰 블랙리스트)",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)

        except Exception:
            return Response("Token is invalid or expired", status.HTTP_401_UNAUTHORIZED)
