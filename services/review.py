from django.shortcuts import get_object_or_404
from django.db.models import Avg
from apps.rental_room.models import RentalRoom
from apps.review.models import Review

def update_average_rating(room_id):
    rental_room = get_object_or_404(RentalRoom, id=room_id)
    aggregated = Review.objects.filter(rental_room=room_id).aggregate(avg_rating=Avg('rating'))
    rental_room.average_rating = aggregated['avg_rating']
    rental_room.save()
