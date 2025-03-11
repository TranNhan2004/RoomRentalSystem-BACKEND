from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend_project.permissions import IsLessor, IsRenter
from apps.rental_room.models import RentalRoom
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

    def _update_average_rating(self, room_id):
        rental_room = get_object_or_404(RentalRoom, id=room_id)
        aggregated = Review.objects.filter(rental_room=room_id).aggregate(avg_rating=Avg('rating'))
        rental_room.average_rating = aggregated['avg_rating']
        rental_room.save(update_fields=['average_rating'])

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        room_id = response.data.get('rental_room') 
        self._update_average_rating(room_id)
        return response

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        original_rating = instance.rating
        response = super().partial_update(request, *args, **kwargs)
        
        new_rating = response.data.get('rating')
        if new_rating != original_rating:
            self._update_average_rating(instance.rental_room.id)
            
        return response

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        room_id = instance.rental_room.id
        response = super().destroy(request, *args, **kwargs)
        
        if room_id:
            self._update_average_rating(room_id)
        return response
