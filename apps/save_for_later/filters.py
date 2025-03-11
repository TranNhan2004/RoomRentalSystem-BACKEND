from django_filters import FilterSet
from .models import SaveForLater


# -----------------------------------------------------------
class SaveForLaterFilter(FilterSet):
    class Meta:
        model = SaveForLater
        fields = ['renter']