import uuid
from django.db import models
from backend_project.utils import upload_to_fn
from apps.user_account.models import CustomUser
from apps.rental_room.models import RentalRoom


# -----------------------------------------------------------
def contract_document_upload_to(instance, filename):
    return upload_to_fn(
        folders_path=f'contracts/room-{instance.rental_room.id}',
        filename=filename,
        instance=instance
    )
    
class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.FileField(upload_to=contract_document_upload_to)
    rental_room = models.ForeignKey(RentalRoom, related_name='contracts', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
# -----------------------------------------------------------
class RentalContract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()
    
    contract = models.ForeignKey(Contract, related_name='rented_contracts', on_delete=models.PROTECT)
    renter = models.ForeignKey(CustomUser, related_name='rented_contracts', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='__RENTAL_CONTRACT__end_date__gt__start_date'
            )
        ]