import requests
from typing import Tuple
from urllib.parse import quote
from django.conf import settings
from backend_project.utils import get_text_without_accents

def get_coords(address: str) -> Tuple[float, float]:
    API_KEY = settings.GOONG_API_KEY
    encode_address = quote(get_text_without_accents(address))    
    response = requests.get(f"https://rsapi.goong.io/geocode?address={encode_address}&api_key={API_KEY}")
    
    if response.status_code == 200:
        first_location = response.json()['results'][0]['geometry']['location']
        return (first_location['lat'], first_location['lng'])
    else:
        print(f"Request is failed with status code: {response.status_code}")


def get_distance_value(source_coords: Tuple[float, float], destination_coords: Tuple[float, float]) -> float:
    API_KEY = settings.GOONG_API_KEY
    response = requests.get(
        f"https://rsapi.goong.io/DistanceMatrix?origins={source_coords[0]},{source_coords[1]}" +
        f"&destinations={destination_coords[0]},{destination_coords[1]}&vehicle=bike&api_key={API_KEY}"
    )
    
    if response.status_code == 200:
        distance_text = response.json()['rows'][0]['elements'][0]['distance']['text']
        return float(distance_text.split()[0]) 
    else:
        print(f"Request is failed with status code: {response.status_code}")