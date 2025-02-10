from rest_framework import viewsets
from .models import SaveForLater
from .serializers import SaveForLaterSerializer


# -----------------------------------------------------------
class SaveForLaterViewSet(viewsets.ModelViewSet):
    queryset = SaveForLater.objects.all()
    serializer_class = SaveForLaterSerializer