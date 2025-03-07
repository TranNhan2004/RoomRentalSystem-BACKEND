from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend_project.permissions import IsRenter
from .models import SaveForLater
from .serializers import SaveForLaterSerializer


# -----------------------------------------------------------
class SaveForLaterViewSet(viewsets.ModelViewSet):
    queryset = SaveForLater.objects.all()
    serializer_class = SaveForLaterSerializer
    permission_classes = [IsAuthenticated, IsRenter]
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)