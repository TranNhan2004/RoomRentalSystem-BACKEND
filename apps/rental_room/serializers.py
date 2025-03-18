from rest_framework.serializers import (
    ModelSerializer, 
    PrimaryKeyRelatedField, 
    ValidationError, 
    TimeField,
    ChoiceField
)
from backend_project.utils import equals_address
from apps.address.models import Commune
from apps.user_account.models import CustomUser
from services.rental_room import update_coords_and_distances_for_room
from .models import (
    RentalRoom, 
    RoomImage, 
    Charges,
    RoomCode,
    MonthlyRoomInvoice,
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
class RoomImageSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = RoomImage
        fields = '__all__'


# -----------------------------------------------------------
class ChargesSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = Charges
        fields = '__all__'
        
    def create(self, validated_data):
        rental_room = validated_data.get('rental_room')
        start_date = validated_data.get('start_date')

        if Charges.objects.filter(end_date__isnull=True, rental_room=rental_room).exists():
            raise ValidationError("There is an existing rental with a null end date.")
        
        if Charges.objects.filter(end_date__gt=start_date, rental_room=rental_room).exists():
            raise ValidationError("Start date is invalid.")
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.end_date:
            raise ValidationError("Cannot update the ended charges list.")
        
        return super().update(instance, validated_data)


# -----------------------------------------------------------
class RoomCodeSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = RoomCode
        fields = '__all__'
        
    def create(self, validated_data):
        rental_room = validated_data.get('rental_room')
        room_codes = RoomCode.objects.filter(rental_room=rental_room)
        
        if room_codes and room_codes.count() >= rental_room.total_number:
            raise ValidationError("Maximum number of room codes reached.")
        
        validated_data['current_occupancy'] = 0
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        is_sharable = validated_data.get('is_sharable')
        max_occupancy = validated_data.get('max_occupancy')
                
        if is_sharable and instance.current_occupancy == instance.max_occupancy:
            raise ValidationError("Cannot make room sharable if current occupancy is max.")
        
        if max_occupancy and max_occupancy < instance.current_occupancy:
            raise ValidationError("Max occupancy cannot be lower than the current occupancy.")
        
        return super().update(instance, validated_data)
    

# -----------------------------------------------------------
class MonthlyRoomInvoiceSerializer(ModelSerializer):
    room_code = PrimaryKeyRelatedField(queryset=RoomCode.objects.all())
    created_mode = ChoiceField(choices=['first', 'auto'], default='auto')

    class Meta:
        model = MonthlyRoomInvoice
        fields = '__all__'
        
    def create(self, validated_data):
        created_mode = validated_data.get('created_mode', 'auto')
        room_code = validated_data.get('room_code')
        
        charges = Charges.objects.filter(
            rental_room=room_code.rental_room, 
            end_date__isnull=True
        ).first()
        if not charges:
            raise ValidationError("Charges list not found for this room.")
        
        has_not_settled_record = MonthlyRoomInvoice.objects.filter(
            room_code=room_code, 
            is_settled=False
        ).exists()
        if has_not_settled_record:
            raise ValidationError("There is an existing unsettled record.")
        
        prev_record = None
        old_kWh_reading = None
        old_m3_reading = None
        
        if created_mode == 'first':
            old_kWh_reading = validated_data.get('old_kWh_reading')
            if not old_kWh_reading:
                raise ValidationError("old_kWh_reading is required when created_mode is 'first'.")
            
            old_m3_reading = validated_data.get('old_m3_reading')
            if not old_m3_reading:
                raise ValidationError("old_m3_reading is required when created_mode is 'first'.")
            
        elif created_mode == 'auto':
            prev_record = MonthlyRoomInvoice.objects.filter(
                room_code=room_code, 
                is_settled=True
            ).order_by('-created_at').first()
            
            if not prev_record:
                raise ValidationError("Previous record not found.")
            
            old_kWh_reading = prev_record.new_kWh_reading
            old_m3_reading = prev_record.new_m3_reading
        
        else:
            raise ValidationError("Invalid created_mode.")

        validated_data['old_kWh_reading'] = old_kWh_reading
        validated_data['old_m3_reading'] = old_m3_reading
            
        if prev_record:
            validated_data['prev_remaining_charge'] = max(prev_record.due_charge - prev_record.paid_charge, 0)
        else:
            validated_data['prev_remaining_charge'] = 0

        validated_data['due_charge'] = (
            validated_data['prev_remaining_charge'] +
            (charges.room_charge if validated_data['continue_renting'] else 0) +
            (validated_data['new_kWh_reading'] - old_kWh_reading) * charges.electricity_charge +
            (validated_data['new_m3_reading'] - old_m3_reading) * charges.water_charge +
            max(charges.wifi_charge, 0) + 
            charges.rubbish_charge
        )
        
        validated_data.pop('created_mode')
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.is_settled:
            raise ValidationError("Cannot update settled record.")
        
        return super().update(instance, validated_data)

        
# -----------------------------------------------------------
class MonitoringRentalSerializer(ModelSerializer):
    room_code = PrimaryKeyRelatedField(queryset=RoomCode.objects.all())
    renter = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = MonitoringRental
        fields = '__all__'        
    
    def create(self, validated_data):
        renter = validated_data.get('renter')
        room_code = validated_data.get('room_code')
        start_date = validated_data.get('start_date')
        
        if MonitoringRental.objects.filter(end_date__isnull=True, room_code=room_code, renter=renter).exists():
            raise ValidationError("Renter already has a rental in progress.")
        
        if MonitoringRental.objects.filter(end_date__gte=start_date, room_code=room_code, renter=renter).exists():
            raise ValidationError("Start date is invalid.")
        
        if room_code.current_occupancy == room_code.max_occupancy:
            raise ValidationError("Room is not available.")
        
        instance = super().create(validated_data)
        
        try:
            room_code_record = RoomCode.objects.get(id=room_code.id)
            room_code_record.current_occupancy += 1
            if room_code_record.current_occupancy == room_code_record.max_occupancy:
                room_code_record.is_sharable = False
                
            room_code_record.save()
            return instance
        
        except RoomCode.DoesNotExist:
            raise ValidationError("Room code with the given id does not exist.")
    
    def update(self, instance, validated_data):
        if instance.end_date:
            raise ValidationError("Cannot update ended rental.")
        
        return super().update(instance, validated_data)