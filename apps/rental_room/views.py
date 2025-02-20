from rest_framework import viewsets, status
from rest_framework.response import Response
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
    
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
# -----------------------------------------------------------
class RentalRoomImageViewSet(viewsets.ModelViewSet):
    queryset = RentalRoomImage.objects.all()
    serializer_class = RentalRoomImageSerializer
    
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# -----------------------------------------------------------
class RoomChargesListViewSet(viewsets.ModelViewSet):
    queryset = RoomChargesList.objects.all()
    serializer_class = RoomChargesListSerializer
    
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# -----------------------------------------------------------
class ElectricityWaterChargesListViewSet(viewsets.ModelViewSet):
    queryset = ElectricityWaterChargesList.objects.all()
    serializer_class = ElectricityWaterChargesListSerializer
    
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# -----------------------------------------------------------
class OtherChargesListViewSet(viewsets.ModelViewSet):
    queryset = OtherChargesList.objects.all()
    serializer_class = OtherChargesListSerializer  
    
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)