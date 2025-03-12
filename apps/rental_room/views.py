from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend_project.permissions import IsLessor
from backend_project.goong_api import get_coords, get_distance_value
from backend_project.utils import equals_address
from apps.address.models import Commune, District, Province
from apps.user_account.models import CustomUser
from apps.distance.models import Distance
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
    
    def _update_coords_and_distances_for_room(self, room_id, commune_id, additional_address):
        commune = get_object_or_404(Commune, id=commune_id)
        district = get_object_or_404(District, id=commune.district.id)
        province = get_object_or_404(Province, id=district.province.id)
            
        room_coords = get_coords(f"{additional_address}, {commune.name}, {district.name}, {province.name}")        
        rental_room = get_object_or_404(RentalRoom, id=room_id)
        rental_room.latitude = room_coords[0]
        rental_room.longitude = room_coords[1]
        rental_room.save()
        
        Distance.objects.filter(rental_room=rental_room.id).delete()
        renters = CustomUser.objects.filter(is_active=True, role='RENTER')

        distances = []
        for renter in renters:
            renter_workplace_coords = (renter.workplace_latitude, renter.workplace_longitude)
            value = get_distance_value(room_coords, renter_workplace_coords)
            distances.append(Distance(renter=renter.id, rental_room=rental_room.id, value=value))

        Distance.objects.bulk_create(distances)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        room_id = response.data.get('id')
        commune_id = response.data.get('commune')
        additional_address = response.data.get('additional_address')
        
        self._update_coords_and_distances_for_room(room_id, commune_id, additional_address)        
        return response
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_commune_id = instance.commune.id
        old_additional_address = instance.additional_address
        old_address = f"{old_additional_address}, {old_commune_id}"

        response = super().partial_update(request, *args, **kwargs)
        room_id = response.data.get('id')

        new_commune_id = response.data.get('commune')
        new_additional_address = response.data.get('additional_address')
        new_address = f"{new_additional_address}, {new_commune_id}"

        if not equals_address(old_address, new_address):
            self._update_coords_and_distances_for_room(room_id, new_commune_id, new_additional_address)

        return response
    
    
# -----------------------------------------------------------
class RentalRoomImageViewSet(viewsets.ModelViewSet):
    queryset = RentalRoomImage.objects.all()
    serializer_class = RentalRoomImageSerializer
    filterset_class = RentalRoomImageFilter
    
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
    
    def create(self, request, *args, **kwargs):
        rental_room = request.data.get('rental_room')
        start_date = request.data.get('start_date')
        
        if not rental_room:
            return Response({"details": "Rental room is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not start_date:
            return Response({"details": "Start date is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if start_date < str(now().date()):
            return Response({"details": "Start date cannot be in the past."}, status=status.HTTP_400_BAD_REQUEST)
        
        if ChargesList.objects.filter(end_date__gte=start_date, rental_room=rental_room).exists():
            return Response({"details": "Start date is invalid."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs) 
        
    
    def list(self, request, *args, **kwargs):
        mode = request.query_params.get('mode', '').lower()
        today = now().date()
        
        self.queryset = self.filter_queryset(self.queryset)

        if mode == 'first':
            filtered_queryset = self.queryset.filter(
                start_date__lte=today,
                end_date__gte=today
            )

            first_data = filtered_queryset.order_by('start_date').first()  
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
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    
    
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
        renter = request.data.get('renter')
        room_code = request.data.get('room_code')
        start_date = request.data.get('start_date')
        
        if not renter:
            return Response({"details": "Renter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not room_code:
            return Response({"details": "Room code is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if start_date < str(now().date()):
            return Response({"details": "Start date cannot be in the past."}, status=status.HTTP_400_BAD_REQUEST)
        
        if MonitoringRental.objects.filter(end_data__gte=start_date, room_code=room_code, renter=renter).exists():
            return Response({"details": "Start date is invalid."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs) 
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)