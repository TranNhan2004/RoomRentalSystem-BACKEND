from django.shortcuts import get_object_or_404
from apps.address.models import Commune, District, Province
from apps.user_account.models import CustomUser
from apps.rental_room.models import RentalRoom
from apps.distance.models import Distance
from .goong_api import get_coords, get_distance_value


def update_coords_and_distances_for_renter(renter_id, workplace_commune_id, workplace_additional_address):
    commune = get_object_or_404(Commune, id=workplace_commune_id)
    district = get_object_or_404(District, id=commune.district.id)
    province = get_object_or_404(Province, id=district.province.id)
        
    renter_wokplace_coords = get_coords(
        f"{workplace_additional_address}, {commune.name}, {district.name}, {province.name}"
    )        
    
    renter = get_object_or_404(CustomUser, id=renter_id)
    renter.workplace_latitude = renter_wokplace_coords[0]
    renter.workplace_longitude = renter_wokplace_coords[1]
    renter.save()
    
    Distance.objects.filter(renter=renter.id).delete()
    rental_rooms = RentalRoom.objects.all()

    distances = []
    for rental_room in rental_rooms:
        room_coords = (rental_room.latitude, rental_room.longitude)
        value = get_distance_value(room_coords, renter_wokplace_coords)
        distances.append(Distance(renter=renter.id, rental_room=renter_id, value=value))

    if len(distances) > 0:
        Distance.objects.bulk_create(distances)