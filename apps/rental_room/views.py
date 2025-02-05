from rest_framework import viewsets

from .models import RentalRoom, ChargesList, RentalRoomImage
from .serializers import RentalRoomSerializer, ChargesListSerializer, RentalRoomImageSerializer


# -----------------------------------------------------------
class RentalRoomViewSet(viewsets.ModelViewSet):
    queryset = RentalRoom.objects.all()
    serializer_class = RentalRoomSerializer
    

# -----------------------------------------------------------
class ChargesListViewSet(viewsets.ModelViewSet):
    queryset = ChargesList.objects.all()
    serializer_class = ChargesListSerializer
    
    
# -----------------------------------------------------------
class RentalRoomImageViewSet(viewsets.ModelViewSet):
    queryset = RentalRoomImage.objects.all()
    serializer_class = RentalRoomImageSerializer