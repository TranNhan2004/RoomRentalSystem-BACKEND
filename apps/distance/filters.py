from django_filters import FilterSet
from .models import Distance


# -----------------------------------------------------------
class DistanceFilter(FilterSet):
    class Meta:
        model = Distance
        fields = ['renter']