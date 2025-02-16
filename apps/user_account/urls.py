from django.urls import path, include
from rest_framework import routers
from .views import (
    CustomUserViewSet, 
    LoginView, 
    CustomTokenRefreshView  
)

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='auth-token-refresh'),
    path('', include(router.urls)),
]