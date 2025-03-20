from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import SearchRoomHistory
from .serializers import SearchRoomHistorySerializer


# -----------------------------------------------------------
class SearchRoomHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchRoomHistory.objects.all()
    serializer_class = SearchRoomHistorySerializer
    permission_classes = [AllowAny]
        
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED) 