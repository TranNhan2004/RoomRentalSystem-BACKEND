from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CustomUserViewSet, LessorViewSet, RenterViewSet, ManagerViewSet


router = routers.DefaultRouter()
router.register(r'base-users', CustomUserViewSet, basename='user')
router.register(r'users/lessors', LessorViewSet, basename='lessor')
router.register(r'users/renters', RenterViewSet, basename='renter')
router.register(r'users/managers', ManagerViewSet, basename='manager')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]