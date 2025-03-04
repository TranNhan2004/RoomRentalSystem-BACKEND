from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import (
    RentalRoom, 
    RentalRoomImage, 
    ChargesList, 
    RoomCode,
    MonthlyChargesDetails,
    MonitoringRental
)
from .serializers import (
    RentalRoomSerializer, 
    RentalRoomImageSerializer,
    ChargesListSerializer,
    RoomCodeSerializer,
    MonthlyChargesDetailsSerializer,
    MonitoringRentalSerializer
)


# -----------------------------------------------------------
class RentalRoomViewSet(viewsets.ModelViewSet):
    queryset = RentalRoom.objects.all()
    serializer_class = RentalRoomSerializer
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    
    
# -----------------------------------------------------------
class RentalRoomImageViewSet(viewsets.ModelViewSet):
    queryset = RentalRoomImage.objects.all()
    serializer_class = RentalRoomImageSerializer
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    

# -----------------------------------------------------------
class ChargesListViewSet(viewsets.ModelViewSet):
    queryset = ChargesList.objects.all()
    serializer_class = ChargesListSerializer
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


# -----------------------------------------------------------
class RoomCodeViewSet(viewsets.ModelViewSet):
    queryset = RoomCode.objects.all()
    serializer_class = RoomCodeSerializer  
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    

# -----------------------------------------------------------
class MonthlyChargesDetailsViewSet(viewsets.ModelViewSet):
    queryset = MonthlyChargesDetails.objects.all()
    serializer_class = MonthlyChargesDetailsSerializer  
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    
    
# -----------------------------------------------------------
class MonitoringRentalViewSet(viewsets.ModelViewSet):
    queryset = MonitoringRental.objects.all()
    serializer_class = MonitoringRentalSerializer  
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)