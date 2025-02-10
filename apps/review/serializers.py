from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Review
from apps.rental_room.models import RentalRoom
from apps.user_account.models import CustomUser


# -----------------------------------------------------------
class ReviewSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    renter = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = Review
        fields = '__all__'