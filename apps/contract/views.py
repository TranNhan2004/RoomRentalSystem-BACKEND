from rest_framework import viewsets
from .models import Contract, RentalContract
from .serializers import ContractSerializer, RentalContractSerializer


# -----------------------------------------------------------
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


# -----------------------------------------------------------
class RentalContractViewSet(viewsets.ModelViewSet):
    queryset = RentalContract.objects.all()
    serializer_class = RentalContractSerializer