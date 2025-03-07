from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from apps.address.models import Commune


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
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)   
        return representation
    

# -----------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': str(self.user.id),
            'role': self.user.role
        }
        return data
    

