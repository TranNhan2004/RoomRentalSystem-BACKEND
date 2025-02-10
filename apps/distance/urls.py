from django.urls import path, include
from rest_framework import routers
from .views import DistanceViewSet

router = routers.DefaultRouter()
router.register(r'distances', DistanceViewSet, basename='distance')

urlpatterns = [
    path('', include(router.urls))
]