from django.urls import path, include
from rest_framework import routers
from .views import (
    RentalRoomViewSet, 
    RoomImageViewSet,
    ChargesViewSet,
    RoomCodeViewSet,
    MonthlyRoomInvoiceViewSet,
    MonitoringRentalViewSet
)

router = routers.DefaultRouter()
router.register(r'rental-rooms', RentalRoomViewSet, basename='rental-room')
router.register(r'room-images', RoomImageViewSet, basename='room-image')
router.register(r'charges', ChargesViewSet, basename='charges')
router.register(r'room-codes', RoomCodeViewSet, basename='room-code')
router.register(r'monthly-room-invoices', MonthlyRoomInvoiceViewSet, basename='monthly-room-invoice')
router.register(r'monitoring-rentals', MonitoringRentalViewSet, basename='monitoring-rental')

urlpatterns = [
    path('', include(router.urls)),
]