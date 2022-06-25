from django.urls import path

from .views import (
    MyTokenBlacklistView,
    MyTokenObtainPairView,
    MyTokenRefreshView,
    MyTokenVerifyView,
    RegisterView,
)

urlpatterns = [
    # path('login/', obtain_auth_token, name='login'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/token/verify/", MyTokenVerifyView.as_view(), name="token_verify"),
    path("login/token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", MyTokenBlacklistView.as_view(), name="token_blacklist"),
]
