from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from backend_project.permissions import IsLessor
from backend_project.utils import today
from .models import (
    RentalRoom, 
    RoomImage, 
    Charges, 
    RoomCode,
    MonthlyRoomInvoice,
    MonitoringRental
)
from .serializers import (
    RentalRoomSerializer, 
    RoomImageSerializer,
    ChargesSerializer,
    RoomCodeSerializer,
    MonthlyRoomInvoiceSerializer,
    MonitoringRentalSerializer
)
from .filters import (
    RentalRoomFilter,
    RoomImageFilter,
    ChargesFilter,
    RoomCodeFilter,
    MonthlyRoomInvoiceFilter,
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
class RoomImageViewSet(viewsets.ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer
    filterset_class = RoomImageFilter
    parser_classes = (MultiPartParser, FormParser)
    
    def get_permissions(self):
        permissions = [IsAuthenticated()]
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions.append(IsLessor())
        
        return permissions
    
    def list(self, request, *args, **kwargs):
        first_only = request.query_params.get('first_only', '').lower() == 'true'
        self.queryset = self.filter_queryset(self.queryset)
        
        if first_only:
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
class ChargesViewSet(viewsets.ModelViewSet):
    queryset = Charges.objects.all()
    serializer_class = ChargesSerializer
    filterset_class = ChargesFilter
    
    def get_permissions(self):
        permissions = [IsAuthenticated()]
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions.append(IsLessor())
        
        return permissions
            
    def list(self, request, *args, **kwargs):
        first_only = request.query_params.get('first_only', '').lower() == 'true'
        self.queryset = self.filter_queryset(self.queryset)

        if first_only:    
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
    
    def partial_update(self, request, *args, **kwargs):
        request.data.pop('remaining_occupancy', None)
        return super().partial_update(request, *args, **kwargs)
    

# -----------------------------------------------------------
class MonthlyRoomInvoiceViewSet(viewsets.ModelViewSet):
    queryset = MonthlyRoomInvoice.objects.all()
    serializer_class = MonthlyRoomInvoiceSerializer  
    filterset_class = MonthlyRoomInvoiceFilter
    
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