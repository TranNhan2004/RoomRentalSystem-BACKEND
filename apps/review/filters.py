from django_filters import FilterSet, DateFilter
from .models import Review


# -----------------------------------------------------------
class ReviewFilter(FilterSet):
    from_created_date = DateFilter(field_name='created_at', lookup_expr='gte')
    to_created_date = DateFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Review
        fields = ['renter', 'rental_room', 'from_created_date', 'to_created_date', 'rating']