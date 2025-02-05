from django.shortcuts import render

# Create your views here.
from .models import Province, District, Commune
from .serializers import ProvinceSerializer, DistrictSerializer, CommuneSerializer
from rest_framework import viewsets


# -----------------------------------------------------------
class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


# -----------------------------------------------------------
class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


# -----------------------------------------------------------
class CommuneViewSet(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer