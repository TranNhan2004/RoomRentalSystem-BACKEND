from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Distance
from .serializers import DistanceSerializer


# -----------------------------------------------------------
class DistanceViewSet(viewsets.ModelViewSet):
    queryset = Distance.objects.all()
    serializer_class = DistanceSerializer
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)