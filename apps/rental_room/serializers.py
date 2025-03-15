from rest_framework.serializers import (
    ModelSerializer, 
    PrimaryKeyRelatedField, 
    ValidationError, 
    TimeField
)
from backend_project.utils import equals_address
from apps.address.models import Commune
from apps.user_account.models import CustomUser
from services.rental_room import update_coords_and_distances_for_room
from .models import (
    RentalRoom, 
    RentalRoomImage, 
    ChargesList,
    RoomCode,
    MonthlyChargesDetails,
    MonitoringRental
)

# -----------------------------------------------------------
class RentalRoomSerializer(ModelSerializer):
    commune = PrimaryKeyRelatedField(queryset=Commune.objects.all())
    lessor = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    manager = PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False, allow_null=True)
    closing_time = TimeField(required=False, allow_null=True)   
    
    class Meta:
        model = RentalRoom
        fields = '__all__'
    
    def is_valid(self, *, raise_exception=True):
        if 'closing_time' in self.initial_data and self.initial_data['closing_time'] == '':
            self.initial_data['closing_time'] = None
            
        return super().is_valid(raise_exception=raise_exception)
    
    def create(self, validated_data):
        instance = super().create(validated_data)
        
        commune = validated_data.get('commune')
        additional_address = validated_data.get('additional_address')
        
        update_coords_and_distances_for_room(instance.id, commune.id, additional_address)
        return instance
    
    def update(self, instance, validated_data):
        old_commune = instance.commune
        old_additional_address = instance.additional_address
        old_address = f"{old_additional_address}, {old_commune.id}" if old_commune else ""
        
        updated_instance = super().update(instance, validated_data)
        
        new_commune = validated_data.get('commune', updated_instance.commune)
        new_additional_address = validated_data.get('additional_address', updated_instance.additional_address)
        new_address = f"{new_additional_address}, {new_commune.id}" if new_commune else ""
        
        if not equals_address(old_address, new_address):
            update_coords_and_distances_for_room(updated_instance.id, new_commune.id, new_additional_address)
        
        return updated_instance


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
        
    def create(self, validated_data):
        rental_room = validated_data.get('rental_room')
        start_date = validated_data.get('start_date')

        if ChargesList.objects.filter(end_date__isnull=True, rental_room=rental_room.id).exists():
            raise ValidationError("There is an existing rental with a null end date.")
        
        if ChargesList.objects.filter(end_date__gte=start_date, rental_room=rental_room.id).exists():
            raise ValidationError("Start date is invalid.")
        
        return super().create(validated_data)


# -----------------------------------------------------------
class RoomCodeSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = RoomCode
        fields = '__all__'
        
    def create(self, validated_data):
        rental_room = validated_data.get('rental_room')
        room_codes_count = RoomCode.objects.filter(rental_room=rental_room).count()
    
        if room_codes_count >= rental_room.total_number:
            raise ValidationError("Maximum number of room codes reached.")
        
        return super().create(validated_data)


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
    
    def create(self, validated_data):
        renter = validated_data.get('renter')
        room_code = validated_data.get('room_code')
        start_date = validated_data.get('start_date')
        
        if MonitoringRental.objects.filter(end_date__isnull=True, room_code=room_code.id, renter=renter.id).exists():
            raise ValidationError("Renter already has a rental in progress.")
        
        if MonitoringRental.objects.filter(end_date__gte=start_date, room_code=room_code.id, renter=renter.id).exists():
            raise ValidationError("Start date is invalid.")
        
        if room_code.remaining_occupancy == 0:
            raise ValidationError("Room is not available.")
        
        instance = super().create(validated_data)
        
        room_code.remaining_occupancy -= 1
        if room_code.remaining_occupancy == 0:
            room_code.is_sharable = False
        room_code.save()
        
        return instance