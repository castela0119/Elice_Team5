from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import (TokenBlacklistSerializer,
                                                  TokenRefreshSerializer,
                                                  TokenVerifySerializer)
from rest_framework_simplejwt.views import (TokenBlacklistView,
                                            TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .models import User
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
        responses={201: "회원가입 성공", 400:"요청형식에 맞지않는 데이터"},
    )
    def post(self, request):
        """
        회원가입 요청 API
        """
        userID = request.data.get("user_ID")
        useremail = request.data.get("email")

        userID = User.objects.filter(user_ID=userID).first()
        useremail = User.objects.filter(email=useremail).first()

        if userID and useremail:
            return Response(
                {"error": "user_ID & email already exist!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        elif userID:
            return Response(
                {"error": "user_ID already exists!"}, status=status.HTTP_400_BAD_REQUEST
            )

        elif useremail:
            return Response(
                {"error": "email already exists!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        else:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                data = {}

                data["response"] = "Registration Successful!"
                data["user_ID"] = user.user_ID
                data["email"] = user.email

                return Response(data, status=status.HTTP_201_CREATED)
            
            else:
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_summary="로그인 시 토큰 발급",
        request_body=MyTokenObtainPairSerializer,
        tags=["user"],
        operation_description="로그인 시 토큰 발급",
        responses={200: "로그인 성공", 401: "없는 회원이거나 비밀번호 틀림"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MyTokenVerifyView(TokenVerifyView):
    serializer_class = TokenVerifySerializer

    @swagger_auto_schema(
        operation_summary="토큰 유효 확인",
        request_body=TokenVerifySerializer,
        tags=["user"],
        operation_description="토큰 유효 확인",
        responses={200: "토큰 유효", 401: "유효하지 않거나 만료된 토큰"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(
        operation_summary="토큰 재발행",
        request_body=TokenRefreshSerializer,
        tags=["user"],
        operation_description="토큰 재발행",
        responses={200: "토큰 재발행 성공", 401: "유효하지 않거나 만료된 토큰"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MyTokenBlacklistView(TokenBlacklistView):
    serializer_class = TokenBlacklistSerializer

    @swagger_auto_schema(
        operation_summary="토큰 블랙리스트",
        request_body=TokenBlacklistSerializer,
        tags=["user"],
        operation_description="토큰 블랙리스트",
        responses={
            200: "로그아웃 성공",
            401: "블랙리스트에 추가된 토큰",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
