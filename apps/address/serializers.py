from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Province, District, Commune


# -----------------------------------------------------------
class ProvinceSerializer(ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

        
# -----------------------------------------------------------
class DistrictSerializer(ModelSerializer):
    province = PrimaryKeyRelatedField(queryset=Province.objects.all())
    
    class Meta:
        model = District
        fields = '__all__'

        
# -----------------------------------------------------------
class CommuneSerializer(ModelSerializer):
    district = PrimaryKeyRelatedField(queryset=District.objects.all())
    
    class Meta:
        model = Commune
        fields = '__all__'