from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import CustomUser, Lessor, Renter, Manager
from apps.address.models import Commune


# -----------------------------------------------------------
class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'citizen_number',
            'phone_number',
            'date_of_birth',
            'gender',
            'avatar',
            'created_at',
            'updated_at',
        )
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['gender'] = instance.get_gender_display()
        return representation
    
        
# -----------------------------------------------------------
class LessorSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = Lessor
        fields = ('user', 'signature_image')
    
        
# -----------------------------------------------------------
class RenterSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    workplace_main_address = PrimaryKeyRelatedField(queryset=Commune.objects.all())
    
    class Meta:
        model = Renter
        fields = ('user', 'signature_image', 'workplace_main_address', 'workplace_additional_address')
    
    
# -----------------------------------------------------------
class ManagerSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = Manager
        fields = ('user',)