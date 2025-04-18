import uuid
from django.db import models
from django.core.validators import MinValueValidator
from apps.user_account.models import CustomUser
from apps.rental_room.models import RentalRoom


# -----------------------------------------------------------
class Distance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    
    rental_room = models.ForeignKey(RentalRoom, related_name='distances', on_delete=models.CASCADE)
    renter = models.ForeignKey(CustomUser, related_name='distances', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['rental_room', 'renter'], 
                name='__DISTANCE__rental_room_renter__unique_together'
            ),
        ]