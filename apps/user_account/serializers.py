from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField, CharField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from backend_project.utils import equals_address, date_time_now
from apps.address.models import Commune
from services.user_account import update_coords_and_distances_for_renter

from .models import CustomUser


# -----------------------------------------------------------
class CustomUserSerializer(ModelSerializer):
    workplace_commune = PrimaryKeyRelatedField(queryset=Commune.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'citizen_number',
            'phone_number',
            'date_of_birth',
            'gender',
            'workplace_commune',
            'workplace_additional_address',
            'role',
            'is_active',
            'last_login',
            'created_at',
            'updated_at',
        )
    
    def validate(self, data):
        role = data.get('role', getattr(self.instance, 'role', None))    
        
        if role != 'RENTER':
            data.pop('workplace_commune', None)
            data.pop('workplace_additional_address', None)
        else:
            workplace_commune = data.get('workplace_commune')
            workplace_additional_address = data.get('workplace_additional_address')
            if not workplace_commune or not workplace_additional_address:
                raise ValidationError('Workplace infomation cannot be null.')
        
        return super().validate(data)
    
    def update(self, instance, validated_data):
        old_commune = instance.workplace_commune
        old_additional_address = instance.workplace_additional_address
        old_workplace_address = f"{old_additional_address}, {old_commune.id}" if old_commune else ""
        
        instance = super().update(instance, validated_data)
        
        if instance.role == 'RENTER':
            new_commune = validated_data.get('workplace_commune', instance.workplace_commune)
            new_additional_address = validated_data.get('workplace_additional_address', instance.workplace_additional_address)
            new_workplace_address = f"{new_additional_address}, {new_commune.id}" if new_commune else ""
            
            if not equals_address(old_workplace_address, new_workplace_address):
                update_coords_and_distances_for_renter(instance.id, new_commune.id, new_additional_address)
        
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)   
        return representation
    

# -----------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):    
    role = CharField(required=True)

    def validate(self, attrs):
        requested_role = attrs.get('role')

        data = super().validate(attrs)
    
        if requested_role != self.user.role:
            raise ValidationError("Invalid role")
        
        self.user.last_login = date_time_now()
        self.user.save()
        
        data['user'] = CustomUserSerializer(self.user).data
        return data
    

