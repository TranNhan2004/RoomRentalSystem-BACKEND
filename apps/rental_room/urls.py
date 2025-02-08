from django.urls import path, include
from rest_framework import routers

from .views import (
    RentalRoomViewSet, 
    RentalRoomImageViewSet,
    RoomChargesListViewSet,
    ElectricityWaterChargesListViewSet,
    OtherChargesListViewSet
)

router = routers.DefaultRouter()
router.register(r'rental-rooms', RentalRoomViewSet, basename='rental-room')
router.register(r'rental-room-images', RentalRoomImageViewSet, basename='rental-room-image')
router.register(r'room-charges-lists', RoomChargesListViewSet, basename='room-charges-list')
router.register(
    r'electricity-water-charges-lists', 
    ElectricityWaterChargesListViewSet, 
    basename='electricity-water-charges-list'
)
router.register(r'other-charges-lists', OtherChargesListViewSet, basename='other-charges-list')

urlpatterns = [
    path('', include(router.urls)),
]