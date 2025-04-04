from random import randint
from django.db.models import Q, Prefetch
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from backend_project.permissions import IsLessor, IsRenter
from backend_project.utils import today
from apps.distance.models import Distance
from apps.save_for_later.models import SaveForLater
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
    
    def get_queryset(self):
        charges_queryset = Charges.objects.filter(
            Q(start_date__lte=today()) &  
            (Q(end_date__gte=today()) | Q(end_date__isnull=True))  
        ).order_by('-start_date')

        renter_id = self.request.query_params.get('_renter', None)
        distance_queryset = Distance.objects.all()
        save_for_later_queryset = SaveForLater.objects.all()
        if renter_id:
            distance_queryset = Distance.objects.filter(renter=renter_id)
            save_for_later_queryset = SaveForLater.objects.filter(renter=renter_id)

        return RentalRoom.objects.prefetch_related(
            'images',
            Prefetch('charges', queryset=charges_queryset, to_attr='filtered_charges'),
            Prefetch('distances', queryset=distance_queryset, to_attr='filtered_distances'),
            Prefetch('saved_items', queryset=save_for_later_queryset, to_attr='filtered_saved_items'),
        )
    
    def get_permissions(self):
        permissions = [IsAuthenticated()]
        
        if self.action in ['create', 'destroy']:
            permissions.append(IsLessor())
        
        return permissions
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsRenter])
    def list_by_ids(self, request, *args, **kwargs):
        recommendation_list = request.data.get('_recommendation_list', None)    
                
        if not isinstance(recommendation_list, list):
            return Response([], status=status.HTTP_200_OK)
        
        if len(recommendation_list) == 0:
            k = settings.RECOMMENDATION_K_CLOSEST_ROOMS
            room_count = k + randint(1, k // 2)

            queryset = self.get_queryset()
            renter_id = request.data.get('_renter', None) 
            if renter_id:
                queryset = queryset.filter(distances__renter=renter_id)
                
            closest_rooms = queryset.order_by('distances__value')[:room_count]

            serializer = self.get_serializer(closest_rooms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
        room_ids = [item['rental_room'] for item in recommendation_list]
        
        queryset = self.get_queryset()
        queryset = queryset.filter(id__in=room_ids)
        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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