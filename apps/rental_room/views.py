from rest_framework import viewsets
from .models import RentalRoom, RentalRoomImage, RoomChargesList, ElectricityWaterChargesList, OtherChargesList
from .serializers import (
    RentalRoomSerializer, 
    RentalRoomImageSerializer,
    RoomChargesListSerializer,
    ElectricityWaterChargesListSerializer,
    OtherChargesListSerializer
)


# -----------------------------------------------------------
class RentalRoomViewSet(viewsets.ModelViewSet):
    queryset = RentalRoom.objects.all()
    serializer_class = RentalRoomSerializer
    
    
# -----------------------------------------------------------
class RentalRoomImageViewSet(viewsets.ModelViewSet):
    queryset = RentalRoomImage.objects.all()
    serializer_class = RentalRoomImageSerializer
    

# -----------------------------------------------------------
class RoomChargesListViewSet(viewsets.ModelViewSet):
    queryset = RoomChargesList.objects.all()
    serializer_class = RoomChargesListSerializer


# -----------------------------------------------------------
class ElectricityWaterChargesListViewSet(viewsets.ModelViewSet):
    queryset = ElectricityWaterChargesList.objects.all()
    serializer_class = ElectricityWaterChargesListSerializer
    

# -----------------------------------------------------------
class OtherChargesListViewSet(viewsets.ModelViewSet):
    queryset = OtherChargesList.objects.all()
    serializer_class = OtherChargesListSerializer  