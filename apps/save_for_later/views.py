from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import SaveForLater
from .serializers import SaveForLaterSerializer


# -----------------------------------------------------------
class SaveForLaterViewSet(viewsets.ModelViewSet):
    queryset = SaveForLater.objects.all()
    serializer_class = SaveForLaterSerializer
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)