from django.urls import path, include
from rest_framework import routers
from .views import (
    CustomUserViewSet, 
    LoginView, 
    CustomTokenRefreshView,
    SendEmailForResetPasswordView,
    ResetPasswordView,
    ChangePasswordView,
    HandleAvatar
)

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='auth-token-refresh'),
    path('auth/reset-password/', SendEmailForResetPasswordView.as_view(), name='auth-reset-password'),
    path('auth/reset-password-confirm/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='auth-reset-password-confirm'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('handle-avatar/', HandleAvatar.as_view(), name='handle-avatar'),
    path('', include(router.urls)),
]