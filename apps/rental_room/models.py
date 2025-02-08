import uuid

from django.db import models
from django.core.validators import MinValueValidator

from backend_project.utils import upload_to_fn

from apps.address.models import Commune
from apps.user_account.models import Lessor, Manager


# -----------------------------------------------------------
class RentalRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)    
    
    commune = models.ForeignKey(Commune, related_name='rental_rooms', on_delete=models.CASCADE)
    additional_address = models.TextField(max_length=512)
    
    closing_time = models.TimeField(null=True)
    
    max_occupancy_per_room = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    
    total_number = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    empty_number = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    
    further_description = models.TextField(max_length=1024, blank=True, null=True)
    
    approved_by = models.ForeignKey(Manager, related_name='approved_rooms', on_delete=models.CASCADE, null=True)
    possessed_by = models.ForeignKey(Lessor, related_name='possessed_rooms', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(empty_number__lte=models.F('total_number')),
                name='__RENTAL_ROOM__empty_number__lte__total_number'
            )
        ]


# -----------------------------------------------------------
def rental_room_image_upload_to(instance, filename):
    return upload_to_fn(
        folders_path=['rental-rooms', f'room-{instance.rental_room.id}'],
        filename=filename
    )
    
class RentalRoomImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_room = models.ForeignKey(RentalRoom, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=rental_room_image_upload_to)


# -----------------------------------------------------------
class RoomChargesList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_room = models.ForeignKey(RentalRoom, related_name='room_charges_list', on_delete=models.CASCADE)
    
    room_charge = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    deposit = models.IntegerField(validators=[MinValueValidator(0)], default=0)
        
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(deposit__lte=models.F('room_charge')),
                name='__ROOM_CHARGES_LIST__deposit__lte__room_charge'
            ),
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='__ROOM_CHARGES_LIST__end_date__gt__start_date'
            )
        ]


# -----------------------------------------------------------
class ElectricityWaterChargesList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_room = models.ForeignKey(RentalRoom, related_name='electricity_water_charges_list', on_delete=models.CASCADE)
    
    ELECTRICITY_CHARGE_TYPE_CHOICES = [
        ('unit', '/kWh'),
        ('person', '/người')
    ]
    electricity_charge_type = models.CharField(
        max_length=8, 
        choices=ELECTRICITY_CHARGE_TYPE_CHOICES, 
        default='unit'
    )
    electricity_charge = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    
    WATER_CHARGE_TYPE_CHOICES = [
        ('unit', '/m3'),
        ('person', '/người'),    
    ]
    water_charge_type = models.CharField(
        max_length=8, 
        choices=WATER_CHARGE_TYPE_CHOICES, 
        default='unit'
    )
    water_charge = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='__ELECTRICITY_WATER_CHARGES_LIST__end_date__gt__start_date'
            )
        ]
    

# -----------------------------------------------------------
class OtherChargesList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_room = models.ForeignKey(RentalRoom, related_name='other_charges_list', on_delete=models.CASCADE)
    
    wifi_charge = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    rubbish_charge = models.IntegerField(validators=[MinValueValidator(0)])
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='__OTHER_CHARGES_LIST__end_date__gt__start_date'
            )
        ]