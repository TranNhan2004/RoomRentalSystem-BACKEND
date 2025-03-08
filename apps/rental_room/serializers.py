from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import (
    RentalRoom, 
    RentalRoomImage, 
    ChargesList,
    RoomCode,
    MonthlyChargesDetails,
    MonitoringRental
)
from apps.address.models import Commune
from apps.user_account.models import CustomUser


# -----------------------------------------------------------
class RentalRoomImageSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = RentalRoomImage
        fields = '__all__'


# -----------------------------------------------------------
class ChargesListSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = ChargesList
        fields = '__all__'
        

# -----------------------------------------------------------
class RoomCodeSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = RoomCode
        fields = '__all__'


# -----------------------------------------------------------
class MonthlyChargesDetailsSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = MonthlyChargesDetails
        fields = '__all__'
        
        
# -----------------------------------------------------------
class MonitoringRentalSerializer(ModelSerializer):
    room_code = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    renter = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = MonitoringRental
        fields = '__all__'
        

# -----------------------------------------------------------
class RentalRoomSerializer(ModelSerializer):
    commune = PrimaryKeyRelatedField(queryset=Commune.objects.all())
    lessor = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    manager = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    images = RentalRoomImageSerializer(many=True, read_only=True)
    charges_lists = ChargesListSerializer(many=True, read_only=True)
    
    class Meta:
        model = RentalRoom
        fields = '__all__'
        