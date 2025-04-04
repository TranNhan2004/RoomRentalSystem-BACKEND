from django_filters import FilterSet, DateFilter, CharFilter, BooleanFilter
from django.db.models import DateField as DateFieldCast, Q, F
from django.db.models.functions import Cast
from backend_project.utils import today
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
    _empty_mode = CharFilter(method='filter__empty_mode')
    _room_charge_range = CharFilter(method='filter__room_charge_range')  

    def filter__empty_mode(self, queryset, name, value):
        if value == 'complete':
            return queryset.filter(room_codes__current_occupancy=0).distinct()
        
        elif value == 'unavailable':
            return queryset.filter(
                (Q(room_codes__current_occupancy=F('room_codes__max_occupancy')) | 
                Q(room_codes__is_shared=False)) &
                Q(room_codes__current_occupancy__gt=0) 
            ).distinct()
        
        elif value == 'shared':
            return queryset.filter(room_codes__is_shared=True).distinct()
        
        return queryset
    
    def filter__room_charge_range(self, queryset, name, value):
        if not value:  
            return queryset
        
        try:
            min_str, max_str = value.split('-')
            min_charge = int(float(min_str) * 1_000_000)  
            if max_str == 'inf':
                max_charge = None  
            else:
                max_charge = int(float(max_str) * 1_000_000)  
        except (ValueError, AttributeError):
            return queryset  
        
        if max_charge is None:
            return queryset.filter(
                Q(charges__end_date__isnull=True) | Q(charges__end_date__gte=today()),
                charges__start_date__lte=today(), 
                charges__room_charge__gte=min_charge  
            ).distinct()
        else:
            return queryset.filter(
                Q(charges__end_date__isnull=True) | Q(charges__end_date__gte=today()),
                charges__start_date__lte=today(),
                charges__room_charge__gte=min_charge,
                charges__room_charge__lte=max_charge
            ).distinct()

    class Meta:
        model = RentalRoom
        fields = ['commune', 'lessor', 'manager', 'manager_is_null', '_empty_mode', '_room_charge_range']
        

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
            Q(end_date__lte=value) | Q(end_date__isnull=True)
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
    from_created_date = DateFilter(method='filter_from_created_date')
    to_created_date = DateFilter(method='filter_to_created_date')

    class Meta:
        model = MonthlyRoomInvoice
        fields = ['room_code', 'is_settled', 'from_created_date', 'to_created_date']

    def filter_from_created_date(self, queryset, name, value):
        return queryset.annotate(
            created_date=Cast('created_at', DateFieldCast())
        ).filter(created_date__gte=value)

    def filter_to_created_date(self, queryset, name, value):
        return queryset.annotate(
            created_date=Cast('created_at', DateFieldCast())
        ).filter(created_date__lte=value)
    
    
        
# -----------------------------------------------------------
class MonitoringRentalFilter(FilterSet):
    from_date = DateFilter(field_name='start_date', lookup_expr='gte')
    to_date = DateFilter(field_name='end_date', method='filter_to_date')

    def filter_to_date(self, queryset, name, value):
        return queryset.filter(
            Q(end_date__lte=value) | Q(end_date__isnull=True)
        )
    
    class Meta:
        model = MonitoringRental
        fields = ['room_code', 'renter', 'from_date', 'to_date']