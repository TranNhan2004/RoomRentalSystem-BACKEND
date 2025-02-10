from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import RentalRoom, RentalRoomImage, RoomChargesList, ElectricityWaterChargesList, OtherChargesList
from apps.address.models import Commune
from apps.user_account.models import CustomUser


# -----------------------------------------------------------
class RentalRoomSerializer(ModelSerializer):
    main_address = PrimaryKeyRelatedField(queryset=Commune.objects.all())
    lessor = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    manager = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = RentalRoom
        fields = '__all__'
        

# -----------------------------------------------------------
class RentalRoomImageSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = RentalRoomImage
        fields = '__all__'


# -----------------------------------------------------------
class RoomChargesListSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = RoomChargesList
        fields = '__all__'
        

# -----------------------------------------------------------
class ElectricityWaterChargesListSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = ElectricityWaterChargesList
        fields = '__all__'


# -----------------------------------------------------------
class OtherChargesListSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = OtherChargesList
        fields = '__all__'