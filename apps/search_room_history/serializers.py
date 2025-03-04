from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import SearchRoomHistory    
from apps.rental_room.models import RentalRoom
from apps.user_account.models import CustomUser


# -----------------------------------------------------------
class SearchRoomHistorySerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    renter = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = SearchRoomHistory
        fields = '__all__'
        