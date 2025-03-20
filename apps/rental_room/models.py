import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from backend_project.utils import upload_to_fn, today
from apps.address.models import Commune
from apps.user_account.models import CustomUser

# -----------------------------------------------------------
class RentalRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)    
    
    commune = models.ForeignKey(Commune, related_name='rental_rooms', on_delete=models.PROTECT)
    additional_address = models.TextField(max_length=512)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    closing_time = models.TimeField(null=True, blank=True)
    total_number = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    average_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    further_description = models.TextField(max_length=1024, null=True, blank=True)
    
    lessor = models.ForeignKey(CustomUser, related_name='possessed_rooms', on_delete=models.PROTECT)
    manager = models.ForeignKey(CustomUser, related_name='approved_rooms', on_delete=models.PROTECT, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

# -----------------------------------------------------------
def room_image_upload_to(instance, filename):
    return upload_to_fn(
        folder_path=f'rooms-images/room-{instance.rental_room.id}',
        filename=filename,
        instance=instance
    )
    
class RoomImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_room = models.ForeignKey(RentalRoom, related_name='images', on_delete=models.PROTECT)
    image = models.ImageField(upload_to=room_image_upload_to)
    

# -----------------------------------------------------------
class Charges(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_room = models.ForeignKey(RentalRoom, related_name='charges', on_delete=models.PROTECT)
    
    room_charge = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    deposit = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    electricity_charge = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    water_charge = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    wifi_charge = models.IntegerField(default=-1, validators=[MinValueValidator(-1)])
    rubbish_charge = models.IntegerField(default=0, validators=[MinValueValidator(0)])
        
    start_date = models.DateField(default=today, validators=[MinValueValidator(today)])
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(end_date__isnull=True) |  
                    models.Q(end_date__gt=models.F('start_date'))  
                ),
                name='__CHARGES__end_date__gt__start_date_or_null'
            ),
        ]



# -----------------------------------------------------------
class RoomCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_room = models.ForeignKey(RentalRoom, related_name='room_codes', on_delete=models.PROTECT)
    
    value = models.CharField(max_length=10)
    current_occupancy = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    max_occupancy = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    is_shared = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(current_occupancy__lte=models.F('max_occupancy')),
                name='__ROOM_CODE__current_occupancy__lte__max_occupancy'
            ),
        ]
    
    
# -----------------------------------------------------------
class MonthlyRoomInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_code = models.ForeignKey(RoomCode, related_name='monthly_room_invoices', on_delete=models.CASCADE)
    
    old_kWh_reading = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    new_kWh_reading = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    old_m3_reading = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    new_m3_reading = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    prev_remaining_charge = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    due_charge = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    paid_charge = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    continue_renting = models.BooleanField(default=True)
    is_settled = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(new_kWh_reading__gte=models.F('old_kWh_reading')),
                name='__MONTHLY_ROOM_INVOICE__new_kWh_reading__gte__old_kWh_reading'
            ),
            models.CheckConstraint(
                check=models.Q(new_m3_reading__gte=models.F('old_m3_reading')),
                name='__MONTHLY_ROOM_INVOICE__new_m3_reading__gte__old_m3_reading'
            )
        ]

    
# -----------------------------------------------------------
class MonitoringRental(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_code = models.ForeignKey(RoomCode, related_name='monitoring_rentals', on_delete=models.CASCADE)
    renter = models.ForeignKey(CustomUser, related_name='rented_rooms', on_delete=models.CASCADE)
        
    start_date = models.DateField(default=today, validators=[MinValueValidator(today)])
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(end_date__isnull=True) |  
                    models.Q(end_date__gt=models.F('start_date'))  
                ),
                name='__MONITORING_RENTAL__end_date__gt__start_date_or_null'
            ),
        ]