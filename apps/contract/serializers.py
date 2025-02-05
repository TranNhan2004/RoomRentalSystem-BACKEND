from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Contract, RentalContract
from apps.user_account.models import Renter
from apps.rental_room.models import RentalRoom


# -----------------------------------------------------------
class ContractSerializer(ModelSerializer):
    rental_room = PrimaryKeyRelatedField(queryset=RentalRoom.objects.all())
    
    class Meta:
        model = Contract
        fields = '__all__'
        

# -----------------------------------------------------------
class RentalContractSerializer(ModelSerializer):
    contract = PrimaryKeyRelatedField(queryset=Contract.objects.all())
    rented_by = PrimaryKeyRelatedField(queryset=Renter.objects.all())
    
    class Meta:
        model = RentalContract
        fields = '__all__'