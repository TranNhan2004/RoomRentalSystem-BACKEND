from django_filters import FilterSet, DateFilter
from django.db.models import DateField as DateFieldCast
from django.db.models.functions import Cast
from apps.review.models import Review

class ReviewFilter(FilterSet):
    from_created_date = DateFilter(method='filter_from_created_date')
    to_created_date = DateFilter(method='filter_to_created_date')

    class Meta:
        model = Review
        fields = ['renter', 'rental_room', 'from_created_date', 'to_created_date', 'rating']

    def filter_from_created_date(self, queryset, name, value):
        return queryset.annotate(
            created_date=Cast('created_at', DateFieldCast())
        ).filter(created_date__gte=value)

    def filter_to_created_date(self, queryset, name, value):
        return queryset.annotate(
            created_date=Cast('created_at', DateFieldCast())
        ).filter(created_date__lte=value)