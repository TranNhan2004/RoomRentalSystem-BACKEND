from django.urls import path, include
from rest_framework import routers
from .views import (
    CustomUserViewSet, 
    LoginView, 
    CustomTokenRefreshView,
    SendEmailForResetPasswordView,
    ResetPasswordView,
    ChangePasswordView,
    SendEmailForRegisterView,
    RegisterView
)

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='auth-token-refresh'),
    path('auth/reset-password/', SendEmailForResetPasswordView.as_view(), name='auth-reset-password'),
    path('auth/reset-password-confirm/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='auth-reset-password-confirm'),
    path('auth/register/', SendEmailForRegisterView.as_view(), name='auth-register'),
    path('auth/activate-account/<str:uidb64>/<str:token>/', RegisterView.as_view(), name='auth-activate-account'),
    path('change-password/<str:id>/', ChangePasswordView.as_view(), name='change-password'),
    path('', include(router.urls)),
]