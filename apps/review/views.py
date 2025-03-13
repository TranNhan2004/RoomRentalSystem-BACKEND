from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend_project.permissions import IsLessor, IsRenter
from services.review import update_average_rating
from .models import Review
from .serializers import ReviewSerializer
from .filters import ReviewFilter


# -----------------------------------------------------------
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions.append(IsRenter())
        else:
            permissions.append(IsRenter() | IsLessor())
        return permissions

    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        room_id = instance.rental_room.id
        response = super().destroy(request, *args, **kwargs)
        
        if room_id:
            update_average_rating(room_id)
        return response
