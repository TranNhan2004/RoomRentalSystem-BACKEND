from django.urls import path, include
from rest_framework import routers
from .views import CustomUserViewSet, CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]