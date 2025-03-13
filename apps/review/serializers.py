from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from apps.rental_room.models import RentalRoom
from apps.user_account.models import CustomUser
from services.review import update_average_rating
from .models import Review


# -----------------------------------------------------------
class ReviewSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    renter = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = Review
        fields = '__all__'
        
    def create(self, validated_data):
        instance = super().create(validated_data)
        update_average_rating(instance.rental_room.id)
        return instance

    def update(self, instance, validated_data):
        original_rating = instance.rating
        instance = super().update(instance, validated_data)
        if instance.rating != original_rating:
            update_average_rating(instance.rental_room.id)
        return instance