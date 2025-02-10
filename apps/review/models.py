import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.rental_room.models import RentalRoom
from apps.user_account.models import CustomUser


# -----------------------------------------------------------
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.CharField(max_length=2048)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    rental_room = models.ForeignKey(RentalRoom, related_name='reviews', on_delete=models.CASCADE)
    renter = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)