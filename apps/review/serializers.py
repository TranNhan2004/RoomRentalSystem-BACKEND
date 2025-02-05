from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Review
from apps.rental_room.models import RentalRoom
from apps.user_account.models import Renter


# -----------------------------------------------------------
class ReviewSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    reviewed_by = PrimaryKeyRelatedField(queryset=Renter.objects.all())
    
    class Meta:
        model = Review
        fields = '__all__'