from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import SaveForLater
from apps.rental_room.models import RentalRoom
from apps.user_account.models import Renter


# -----------------------------------------------------------
class SaveForLaterSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    reviewed_by = PrimaryKeyRelatedField(queryset=Renter.objects.all())
    
    class Meta:
        model = SaveForLater
        fields = '__all__'