from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from apps.address.models import Commune


# -----------------------------------------------------------
class CustomUserSerializer(ModelSerializer):
    workplace_commune = PrimaryKeyRelatedField(queryset=Commune.objects.all(), required=False)
    
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
            'avatar',
            'workplace_commune',
            'workplace_additional_address',
            'role',
            'is_active',
            'created_at',
            'updated_at',
        )
    
    def validate(self, data):
        role = data.get('role', getattr(self.instance, 'role', None))
        workplace_commune = data.get('workplace_commune')
        workplace_additional_address = data.get('workplace_additional_address')
        
        if role != 'R':
            data.pop('workplace_commune', None)
            data.pop('workplace_additional_address', None)
        else:
            if not workplace_commune or not workplace_additional_address:
                raise ValidationError('Thông tin địa chỉ làm việc phải được nhập!')
        
        return data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)   
        representation['gender'] = instance.get_gender_display()
        representation['role'] = instance.get_role_display()
        return representation
    

# -----------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['id'] = str(self.user.id)
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['role'] = self.user.role
        return data
    

