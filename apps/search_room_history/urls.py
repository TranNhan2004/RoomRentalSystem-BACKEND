from django.urls import path, include
from rest_framework import routers
from .views import SearchRoomHistoryViewSet

router = routers.DefaultRouter()
router.register(r'search-room-histories', SearchRoomHistoryViewSet, basename='search-room-history')

urlpatterns = [
    path('', include(router.urls)),
]