from django.urls import path, include
from rest_framework import routers

from .views import ProvinceViewSet, DistrictViewSet, CommuneViewSet


router = routers.DefaultRouter()
router.register(r'provinces', ProvinceViewSet, basename='province')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'communes', CommuneViewSet, basename='commune')

urlpatterns = [
    path('', include(router.urls))
]