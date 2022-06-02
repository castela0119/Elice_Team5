from .models import MyUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer, TokenBlacklistSerializer, TokenRefreshSerializer
from rest_framework.exceptions import ValidationError
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['user_ID', 'email', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    
    def save(self):

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if MyUser.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})

        account = MyUser(email=self.validated_data['email'], user_ID=self.validated_data['user_ID'])
        account.set_password(password)
        account.save()

        return account


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data['user_ID'] = self.user.get_username()
        return data

class MyTokenVerifySerializer(TokenVerifySerializer):
    token = serializers.CharField()

class MyTokenBlacklistSerializer(TokenBlacklistSerializer):
    refresh = serializers.CharField()

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)