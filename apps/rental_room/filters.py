from django.db import models
from django_filters import FilterSet, BooleanFilter, DateFilter
from .models import (
    RentalRoom,
    RoomImage,
    Charges,
    RoomCode,
    MonthlyRoomInvoice,
    MonitoringRental
)


# -----------------------------------------------------------
class RentalRoomFilter(FilterSet):    
    manager_is_null = BooleanFilter(field_name='manager', lookup_expr='isnull')
    is_empty = BooleanFilter(method='filter_is_empty')
    
    def filter_is_empty(self, queryset, name, value):
        if value:
            return queryset.filter(
                room_codes__is_shareable=True,              
                room_codes__remaining_occupancy__gt=0         
            ).distinct()
        return queryset
    
    class Meta:
        model = RentalRoom
        fields = ['commune', 'lessor', 'manager', 'manager_is_null', 'is_empty']
        

# -----------------------------------------------------------
class RoomImageFilter(FilterSet):    
    class Meta:
        model = RoomImage
        fields = ['rental_room']


# -----------------------------------------------------------
class ChargesFilter(FilterSet):  
    from_date = DateFilter(field_name='start_date', lookup_expr='gte')
    to_date = DateFilter(field_name='end_date', method='filter_to_date')

    def filter_to_date(self, queryset, name, value):
        return queryset.filter(
            models.Q(end_date__lte=value) | models.Q(end_date__isnull=True)
        )
  
    class Meta:
        model = Charges
        fields = ['rental_room', 'from_date', 'to_date']


# -----------------------------------------------------------
class RoomCodeFilter(FilterSet):    
    class Meta:
        model = RoomCode
        fields = ['rental_room']
        
        
# -----------------------------------------------------------
class MonthlyRoomInvoiceFilter(FilterSet):
    from_created_date = DateFilter(field_name='created_at', lookup_expr='gte')
    to_created_date = DateFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = MonthlyRoomInvoice
        fields = ['room_code', 'is_settled', 'from_created_date', 'to_created_date']
        

# -----------------------------------------------------------
class MonitoringRentalFilter(FilterSet):
    from_date = DateFilter(field_name='start_date', lookup_expr='gte')
    to_date = DateFilter(field_name='end_date', method='filter_to_date')

    def filter_to_date(self, queryset, name, value):
        return queryset.filter(
            models.Q(end_date__lte=value) | models.Q(end_date__isnull=True)
        )
    
    class Meta:
        model = MonitoringRental
        fields = ['room_code', 'renter', 'from_date', 'to_date']