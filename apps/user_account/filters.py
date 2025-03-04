from django_filters import (
    FilterSet,
    MultipleChoiceFilter,
    BooleanFilter,
    CharFilter
)

from backend_project.choices import ROLE_CHOICES
from .models import CustomUser


# -----------------------------------------------------------
class CustomUserFilter(FilterSet):
    role_include = MultipleChoiceFilter(field_name='role', choices=ROLE_CHOICES, conjoined=False)  
    
    class Meta:
        model = CustomUser
        fields = ['role_include', 'is_active']
    