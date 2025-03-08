from django_filters import FilterSet, BooleanFilter
from .models import (
    RentalRoom,
    RentalRoomImage,
    ChargesList,
    RoomCode,
    MonthlyChargesDetails,
    MonitoringRental
)


# -----------------------------------------------------------
class RentalRoomFilter(FilterSet):    
    manager_is_null = BooleanFilter(field_name='manager', lookup_expr='isnull')
    
    class Meta:
        model = RentalRoom
        fields = ['commune', 'lessor', 'manager', 'manager_is_null']
        

# -----------------------------------------------------------
class RentalRoomImageFilter(FilterSet):    
    class Meta:
        model = RentalRoomImage
        fields = ['rental_room']


# -----------------------------------------------------------
class ChargesListFilter(FilterSet):    
    class Meta:
        model = ChargesList
        fields = ['rental_room']


# -----------------------------------------------------------
class RoomCodeFilter(FilterSet):    
    class Meta:
        model = RoomCode
        fields = ['rental_room']
        
        
# -----------------------------------------------------------
class MonthlyChargesDetailsFilter(FilterSet):
    class Meta:
        model = MonthlyChargesDetails
        fields = ['room_code']
        

# -----------------------------------------------------------
class MonitoringRentalFilter(FilterSet):
    class Meta:
        model = MonitoringRental
        fields = ['room_code', 'renter']