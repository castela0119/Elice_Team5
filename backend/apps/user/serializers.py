from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_ID", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        password = self.validated_data["password"]

        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "Email already exists!"})

        user = User(
            email=self.validated_data["email"], user_ID=self.validated_data["user_ID"]
        )
        user.set_password(password)
        user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user_ID"] = self.user.get_username()
        return data
