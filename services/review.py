from django.shortcuts import get_object_or_404
from django.db.models import Avg
from apps.rental_room.models import RentalRoom
from apps.review.models import Review

def update_average_rating(room_id):
    rental_room = get_object_or_404(RentalRoom, id=room_id)
    reviews = Review.objects.filter(rental_room=room_id)
    
    if len(reviews) > 0:
        aggregated = reviews.aggregate(avg_rating=Avg('rating'))
    else:
        aggregated = {'avg_rating': 0}
        
    rental_room.average_rating = aggregated['avg_rating']
    rental_room.save()
