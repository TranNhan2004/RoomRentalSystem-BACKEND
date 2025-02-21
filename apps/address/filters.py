from django_filters import FilterSet
from .models import District, Commune


# -----------------------------------------------------------
class DistrictFilter(FilterSet):
    class Meta:
        model = District
        fields = ['province']
        

# -----------------------------------------------------------
class CommuneFilter(FilterSet):
    class Meta:
        model = Commune
        fields = ['district']