from django.shortcuts import get_object_or_404
from apps.address.models import Commune, District, Province
from apps.user_account.models import CustomUser
from apps.rental_room.models import RentalRoom
from apps.distance.models import Distance 
from .goong_api import get_coords, get_distance_value

def update_coords_and_distances_for_room(room_id, commune_id, additional_address):
    commune = get_object_or_404(Commune, id=commune_id)
    district = get_object_or_404(District, id=commune.district.id)
    province = get_object_or_404(Province, id=district.province.id)
    
    room_coords = get_coords(f"{additional_address}, {commune.name}, {district.name}, {province.name}")
    
    rental_room = get_object_or_404(RentalRoom, id=room_id)
    rental_room.latitude = room_coords[0]
    rental_room.longitude = room_coords[1]
    rental_room.save()
    
    Distance.objects.filter(rental_room=rental_room.id).delete()
    
    renters = CustomUser.objects.filter(is_active=True, role='RENTER')
    distances = []
    for renter in renters:
        renter_workplace_coords = (renter.workplace_latitude, renter.workplace_longitude)
        value = get_distance_value(room_coords, renter_workplace_coords)
        distances.append(Distance(renter=renter.id, rental_room=rental_room.id, value=value))
    
    if len(distances) > 0:
        Distance.objects.bulk_create(distances)
