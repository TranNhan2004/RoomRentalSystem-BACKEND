import uuid

from django.db import models

from apps.rental_room.models import RentalRoom
from apps.user_account.models import Renter


# -----------------------------------------------------------
class SaveForLater(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.CharField(max_length=512, null=True, blank=True)
    
    rental_room = models.ForeignKey(RentalRoom, related_name='saved_items', on_delete=models.CASCADE)
    saved_by = models.ForeignKey(Renter, related_name='saved_items', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)