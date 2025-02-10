from rest_framework import viewsets
from .models import Distance
from .serializers import DistanceSerializer


# -----------------------------------------------------------
class DistanceViewSet(viewsets.ModelViewSet):
    queryset = Distance.objects.all()
    serializer_class = DistanceSerializer