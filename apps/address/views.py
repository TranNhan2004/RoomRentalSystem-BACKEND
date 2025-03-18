from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from backend_project.permissions import IsManager
from .models import Province, District, Commune
from .serializers import ProvinceSerializer, DistrictSerializer, CommuneSerializer
from .filters import DistrictFilter, CommuneFilter


# -----------------------------------------------------------
class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        
        else:
            permissions = [IsAuthenticated()]
            if self.action in ['create', 'update', 'partial_update', 'destroy']:
                permissions.append(IsManager())
            return permissions
            
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    


# -----------------------------------------------------------
class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filterset_class = DistrictFilter
    
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        
        else:
            permissions = [IsAuthenticated()]
            if self.action in ['create', 'update', 'partial_update', 'destroy']:
                permissions.append(IsManager())
            return permissions
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


# -----------------------------------------------------------
class CommuneViewSet(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    filterset_class = CommuneFilter
    
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        
        else:
            permissions = [IsAuthenticated()]
            if self.action in ['create', 'update', 'partial_update', 'destroy']:
                permissions.append(IsManager())
            return permissions
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)