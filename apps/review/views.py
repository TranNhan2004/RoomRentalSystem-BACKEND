from django.db.models import Avg
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend_project.permissions import IsLessor, IsRenter
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

    def update_average_rating(self, rental_room):
        aggregated = Review.objects.filter(rental_room=rental_room).aggregate(avg_rating=Avg('rating'))
        rental_room.average_rating = aggregated['avg_rating']
        rental_room.save(update_fields=['average_rating'])

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        rental_room = response.data.get('rental_room') 
        if rental_room:
            self.update_average_rating(rental_room)
        return response

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        original_rating = instance.rating
        response = super().partial_update(request, *args, **kwargs)
        
        if 'rating' in request.data:
            new_rating = response.data.get('rating')
            if new_rating != original_rating:
                rental_room = instance.rental_room
                if rental_room:
                    self.update_average_rating(rental_room)
        return response

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        rental_room = instance.rental_room
        response = super().destroy(request, *args, **kwargs)
        
        if rental_room:
            self.update_average_rating(rental_room)
        return response
