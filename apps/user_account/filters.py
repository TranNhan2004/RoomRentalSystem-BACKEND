from django_filters import FilterSet, UUIDFilter, MultipleChoiceFilter
from backend_project.choices import ROLE_CHOICES
from .models import CustomUser


class CustomUserFilter(FilterSet):
    id_not = UUIDFilter(field_name='id', lookup_expr='exact', exclude=True)
    role_include = MultipleChoiceFilter(field_name='role', choices=ROLE_CHOICES, conjoined=False)
    
    # def filter_id_not(self, queryset, name, value):
    #     return queryset.exclude(id=value)

    class Meta:
        model = CustomUser
        fields = ['id_not', 'role_include', 'is_active']