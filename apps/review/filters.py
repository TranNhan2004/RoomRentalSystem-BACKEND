from django_filters import FilterSet
from .models import Review


# -----------------------------------------------------------
class ReviewFilter(FilterSet):
    class Meta:
        model = Review
        fields = ['renter', 'rental_room']