from django.conf import settings
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from apps.rental_room.models import RentalRoom
from apps.user_account.models import CustomUser
from .models import SearchRoomHistory    

# -----------------------------------------------------------
class SearchRoomHistorySerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    renter = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = SearchRoomHistory
        fields = '__all__'
        
    def create(self, validated_data):
        instance = super().create(validated_data)
        renter = validated_data.get('renter')
        search_history_qs = SearchRoomHistory.objects.filter(renter=renter.id).order_by('created_at')
        
        max_count = settings.MAX_SEARCH_ROOM_HISTORY_COUNT
        count = search_history_qs.count()
        
        if count > max_count:
            ids_to_delete = list(search_history_qs.values_list('id', flat=True)[:count - max_count])
            SearchRoomHistory.objects.filter(id__in=ids_to_delete).delete()
            
        return instance
        