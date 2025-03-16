from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from backend_project.permissions import IsLessor
from backend_project.utils import today
from .models import (
    RentalRoom, 
    RentalRoomImage, 
    ChargesList, 
    RoomCode,
    MonthlyChargesDetails,
    MonitoringRental
)
from .serializers import (
    RentalRoomSerializer, 
    RentalRoomImageSerializer,
    ChargesListSerializer,
    RoomCodeSerializer,
    MonthlyChargesDetailsSerializer,
    MonitoringRentalSerializer
)
from .filters import (
    RentalRoomFilter,
    RentalRoomImageFilter,
    ChargesListFilter,
    RoomCodeFilter,
    MonthlyChargesDetailsFilter,
    MonitoringRentalFilter,
)


# -----------------------------------------------------------
class RentalRoomViewSet(viewsets.ModelViewSet):
    queryset = RentalRoom.objects.all()
    serializer_class = RentalRoomSerializer
    filterset_class = RentalRoomFilter
    
    def get_permissions(self):
        permissions = [IsAuthenticated()]
        
        if self.action in ['create', 'destroy']:
            permissions.append(IsLessor())
        
        return permissions
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    
    
# -----------------------------------------------------------
class RentalRoomImageViewSet(viewsets.ModelViewSet):
    queryset = RentalRoomImage.objects.all()
    serializer_class = RentalRoomImageSerializer
    filterset_class = RentalRoomImageFilter
    parser_classes = (MultiPartParser, FormParser)
    
    def get_permissions(self):
        permissions = [IsAuthenticated()]
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions.append(IsLessor())
        
        return permissions
    
    def list(self, request, *args, **kwargs):
        mode = request.query_params.get('mode', '').lower()
        self.queryset = self.filter_queryset(self.queryset)
        
        if mode == 'first':
            first_data = self.queryset.first()
            if first_data:
                serializer = self.get_serializer(first_data)
                return Response([serializer.data], status=status.HTTP_200_OK)
            return Response([], status=status.HTTP_200_OK)
        
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    

# -----------------------------------------------------------
class ChargesListViewSet(viewsets.ModelViewSet):
    queryset = ChargesList.objects.all()
    serializer_class = ChargesListSerializer
    filterset_class = ChargesListFilter
    
    def get_permissions(self):
        permissions = [IsAuthenticated()]
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions.append(IsLessor())
        
        return permissions
            
    def list(self, request, *args, **kwargs):
        mode = request.query_params.get('mode', '').lower()
        self.queryset = self.filter_queryset(self.queryset)

        if mode == 'first':
            filtered_queryset = self.queryset.filter(
                start_date__lte=today()
            ).filter(
                end_date__isnull=True
            )

            first_data = filtered_queryset.first()
            
            if first_data:
                serializer = self.get_serializer(first_data)
                return Response([serializer.data], status=status.HTTP_200_OK)
            
            return Response([], status=status.HTTP_200_OK)
        
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


# -----------------------------------------------------------
class RoomCodeViewSet(viewsets.ModelViewSet):
    queryset = RoomCode.objects.all()
    serializer_class = RoomCodeSerializer  
    filterset_class = RoomCodeFilter
    
    def get_permissions(self):
        permissions = [IsAuthenticated()]
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions.append(IsLessor())
        
        return permissions
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        request.data.pop('remaining_occupancy', None)
        return super().partial_update(request, *args, **kwargs)
    

# -----------------------------------------------------------
class MonthlyChargesDetailsViewSet(viewsets.ModelViewSet):
    queryset = MonthlyChargesDetails.objects.all()
    serializer_class = MonthlyChargesDetailsSerializer  
    filterset_class = MonthlyChargesDetailsFilter
    
    def get_permissions(self):
        permissions = [IsAuthenticated()]
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions.append(IsLessor())
        
        return permissions
    
    def create(self, request, *args, **kwargs):
        request.data.pop('prev_remaining_charge', None)
        request.data.pop('due_charge', None)
        request.data.pop('paid_charge', None)
        request.data.pop('is_settled', None)
        request.data.pop('created_at', None)
        request.data.pop('updated_at', None)
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        request.data.pop('prev_remaining_charge', None)
        request.data.pop('due_charge', None)
        request.data.pop('created_at', None)
        request.data.pop('updated_at', None)
        return super().partial_update(request, *args, **kwargs)
    
    
# -----------------------------------------------------------
class MonitoringRentalViewSet(viewsets.ModelViewSet):
    queryset = MonitoringRental.objects.all()
    serializer_class = MonitoringRentalSerializer  
    filterset_class = MonitoringRentalFilter
    
    def get_permissions(self):
        permissions = [IsAuthenticated()]
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions.append(IsLessor())
        
        return permissions
    
    def create(self, request, *args, **kwargs):
        request.data.pop('end_date', None)
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)