import uuid
from django.db import models
from apps.rental_room.models import RentalRoom
from apps.user_account.models import CustomUser


# -----------------------------------------------------------
class SaveForLater(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.CharField(max_length=512, null=True, blank=True)
    
    rental_room = models.ForeignKey(RentalRoom, related_name='saved_items', on_delete=models.CASCADE)
    renter = models.ForeignKey(CustomUser, related_name='saved_items', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['rental_room', 'renter'], 
                name='__SAVE_FOR_LATER__rental_room_renter__unique_together'
            ),
        ]