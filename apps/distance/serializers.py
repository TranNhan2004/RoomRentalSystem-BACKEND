from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Distance
from apps.user_account.models import CustomUser
from apps.rental_room.models import RentalRoom


# -----------------------------------------------------------
class DistanceSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    renter = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = Distance
        fields = '__all__'