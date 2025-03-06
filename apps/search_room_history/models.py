import uuid

from django.db import models
from django.core.validators import MinValueValidator
from apps.rental_room.models import RentalRoom
from apps.user_account.models import CustomUser


# -----------------------------------------------------------
class SearchRoomHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_room = models.ForeignKey(RentalRoom, related_name='search_room_history', on_delete=models.PROTECT)
    renter = models.ForeignKey(CustomUser, related_name='search_room_history', on_delete=models.PROTECT)
    
    weight = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    
    created_at = models.DateTimeField(auto_now_add=True)