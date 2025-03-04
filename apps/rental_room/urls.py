from django.urls import path, include
from rest_framework import routers
from .views import (
    RentalRoomViewSet, 
    RentalRoomImageViewSet,
    ChargesListViewSet,
    RoomCodeViewSet,
    MonthlyChargesDetailsViewSet,
    MonitoringRentalViewSet
)

router = routers.DefaultRouter()
router.register(r'rental-rooms', RentalRoomViewSet, basename='rental-room')
router.register(r'rental-room-images', RentalRoomImageViewSet, basename='rental-room-image')
router.register(r'charges-lists', ChargesListViewSet, basename='charges-list')
router.register(r'room-codes', RoomCodeViewSet, basename='room-code')
router.register(r'monthly-charges-details', MonthlyChargesDetailsViewSet, basename='monthly-charges-details')
router.register(r'monitoring-rentals', MonitoringRentalViewSet, basename='monitoring-rental')

urlpatterns = [
    path('', include(router.urls)),
]