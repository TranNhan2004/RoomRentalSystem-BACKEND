from django.urls import path, include
from rest_framework import routers
from .views import (
    CustomUserViewSet, 
    LoginView, 
    CheckLoginStatusView,
    CustomTokenRefreshView,  
    LogoutView
)

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('check-login-status/', CheckLoginStatusView.as_view(), name='check-login-status'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]