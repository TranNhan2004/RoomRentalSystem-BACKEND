from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Contract, RentalContract
from .serializers import ContractSerializer, RentalContractSerializer


# -----------------------------------------------------------
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# -----------------------------------------------------------
class RentalContractViewSet(viewsets.ModelViewSet):
    queryset = RentalContract.objects.all()
    serializer_class = RentalContractSerializer
    
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)