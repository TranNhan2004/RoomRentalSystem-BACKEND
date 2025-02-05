from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import RentalRoom, ChargesList, RentalRoomImage
from apps.address.models import Commune
from apps.user_account.models import Lessor, Manager


# -----------------------------------------------------------
class RentalRoomSerializer(ModelSerializer):
    main_address = PrimaryKeyRelatedField(queryset=Commune.objects.all())
    approved_by = PrimaryKeyRelatedField(queryset=Manager.objects.all())
    possesed_by = PrimaryKeyRelatedField(queryset=Lessor.objects.all())
    
    class Meta:
        model = RentalRoom
        fields = '__all__'
        
        
# -----------------------------------------------------------
class ChargesListSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = ChargesList
        fields = '__all__'
        
        
# -----------------------------------------------------------
class RentalRoomImageSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = RentalRoomImage
        fields = '__all__'