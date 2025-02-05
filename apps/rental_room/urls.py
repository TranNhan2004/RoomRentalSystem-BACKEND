from django.urls import path, include
from rest_framework import routers

from .views import RentalRoomViewSet, ChargesListViewSet, RentalRoomImageViewSet

router = routers.DefaultRouter()
router.register(r'rental-rooms', RentalRoomViewSet, basename='rental-room')
router.register(r'charges-list', ChargesListViewSet, basename='charges-list')
router.register(r'rental-room-images', RentalRoomImageViewSet, basename='rental-room-image')

urlpatterns = [
    path('', include(router.urls)),
]