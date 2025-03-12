from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend_project.permissions import IsRenter
from .models import SearchRoomHistory
from .serializers import SearchRoomHistorySerializer


# -----------------------------------------------------------
class SearchRoomHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchRoomHistory.objects.all()
    serializer_class = SearchRoomHistorySerializer
    permission_classes = [IsAuthenticated, IsRenter]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        renter_id = response.data.get('renter')
        search_room_histories = SearchRoomHistory.objects.filter(renter=renter_id).order_by('created_at')
        
        max_count = settings.MAX_SEARCH_ROOM_HISTORY_COUNT
        
        count = search_room_histories.count()
        if count > max_count:
            search_room_histories[:count - max_count].delete()
        return response
 
    
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED) 