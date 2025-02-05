from django.urls import path, include
from rest_framework import routers

from .views import ContractViewSet, RentalContractViewSet

router = routers.DefaultRouter()
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'rental-contracts', RentalContractViewSet, basename='rental-contract')

urlpatterns = [
    path('', include(router.urls))
]