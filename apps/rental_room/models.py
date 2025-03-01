import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from backend_project.utils import upload_to_fn
from apps.address.models import Commune
from apps.user_account.models import CustomUser
from storages.backends.s3boto3 import S3Boto3Storage


# -----------------------------------------------------------
class RentalRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)    
    
    commune = models.ForeignKey(Commune, related_name='rental_rooms', on_delete=models.PROTECT)
    additional_address = models.TextField(max_length=512)
    
    closing_time = models.TimeField(null=True)
    
    max_occupancy_per_room = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    
    total_number = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    empty_number = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    
    average_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    further_description = models.TextField(max_length=1024, blank=True, null=True)
    
    lessor = models.ForeignKey(CustomUser, related_name='possessed_rooms', on_delete=models.PROTECT)
    manager = models.ForeignKey(CustomUser, related_name='approved_rooms', on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=False)
    
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
        folders_path=f'rental-rooms-images/room-{instance.rental_room.id}',
        filename=filename,
        instance=instance
    )
    
class RentalRoomImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_room = models.ForeignKey(RentalRoom, related_name='images', on_delete=models.PROTECT)
    image = models.ImageField(storage=S3Boto3Storage(), upload_to=rental_room_image_upload_to)
    
    def delete(self, *args, **kwargs):
        if self.avatar:
            self.avatar.delete(save=False)  

        super(RentalRoomImage, self).delete(*args, **kwargs)


# -----------------------------------------------------------
class RoomChargesList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_room = models.ForeignKey(RentalRoom, related_name='room_charges_list', on_delete=models.PROTECT)
    
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
    rental_room = models.ForeignKey(RentalRoom, related_name='electricity_water_charges_list', on_delete=models.PROTECT)
    
    ELECTRICITY_CHARGE_TYPE_CHOICES = [
        ('UNIT', '/kWh'),
        ('PERSON', '/người')
    ]
    electricity_charge_type = models.CharField(
        max_length=8, 
        choices=ELECTRICITY_CHARGE_TYPE_CHOICES, 
        default='UNIT'
    )
    electricity_charge = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    
    WATER_CHARGE_TYPE_CHOICES = [
        ('UNIT', '/m3'),
        ('PERSON', '/người'),    
    ]
    water_charge_type = models.CharField(
        max_length=8, 
        choices=WATER_CHARGE_TYPE_CHOICES, 
        default='UNIT'
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
    rental_room = models.ForeignKey(RentalRoom, related_name='other_charges_list', on_delete=models.PROTECT)
    
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