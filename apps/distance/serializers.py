from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Distance
from apps.user_account.models import Renter
from apps.rental_room.models import RentalRoom


# -----------------------------------------------------------
class DistanceSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    renter = PrimaryKeyRelatedField(queryset=Renter.objects.all())
    
    class Meta:
        model = Distance
        fields = '__all__'