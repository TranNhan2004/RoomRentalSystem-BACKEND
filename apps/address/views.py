from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Province, District, Commune
from .serializers import ProvinceSerializer, DistrictSerializer, CommuneSerializer
from .filters import DistrictFilter, CommuneFilter


# -----------------------------------------------------------
class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# -----------------------------------------------------------
class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filterset_class = DistrictFilter
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# -----------------------------------------------------------
class CommuneViewSet(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)