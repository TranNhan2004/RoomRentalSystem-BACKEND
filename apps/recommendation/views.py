import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

from typing import List, Dict

from django.shortcuts import get_list_or_404, get_object_or_404
from django.conf import settings
from django.db.models import Q

from backend_project.utils import today

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from apps.rental_room.models import RentalRoom, Charges
from apps.search_room_history.models import SearchRoomHistory
from apps.distance.models import Distance


# -----------------------------------------------------------
class GetRecommendationsView(APIView):
    def _min_max_scaler_with_rate(self, data: List[float], scale_rate: float):
        data = np.array(data)  
        old_min = np.min(data)
        old_max = np.max(data)

        if old_min == old_max:
            return np.full_like(data, fill_value=scale_rate, dtype=float)  
        
        scaled_data = (data - old_min) / (old_max - old_min)
        scaled_data = scaled_data * scale_rate
        
        return scaled_data
    
    def _get_weights_of_searched_data(self, renter_id: str) -> Dict[str, float]:
        search_room_histories = SearchRoomHistory.objects.filter(renter=renter_id)
        
        weights = {}
        for search_room_history in search_room_histories:
            room_id = search_room_history.rental_room.id
            weight = search_room_history.weight            
            if room_id not in weights:
                weights[room_id] = weight
            else:
                weights[room_id] += weight            
        return weights
    
    def _get_scaled_rental_rooms_df(self, renter_id: str):
        rental_rooms = RentalRoom.objects.filter(manager__isnull=False)
        
        rental_rooms_data = []
        for rental_room in rental_rooms:
            distance = get_object_or_404(Distance, rental_room=rental_room.id, renter=renter_id)
            charges = get_object_or_404(
                Charges, 
                Q(end_date__isnull=True) | Q(end_date__gte=today()),
                rental_room=rental_room.id, 
                start_date__lte=today(),
            )
            
            rental_rooms_data.append({
                'id': rental_room.id,
                'room_charge': charges.room_charge,
                'electricity_charge': charges.electricity_charge,
                'water_charge': charges.water_charge,
                'wifi_charge': charges.wifi_charge,
                'rubbish_charge': charges.rubbish_charge,
                'distance_value': distance.value,
            })
        
        df = pd.DataFrame(rental_rooms_data)

        if len(df) > 0:        
            scaled_columns_and_rate = [
                ('room_charge', settings.RECOMMENDATION_ROOM_CHARGE_SCALE_RATE),
                ('electricity_charge', settings.RECOMMENDATION_ELECTRICITY_CHARGE_SCALE_RATE),
                ('water_charge', settings.RECOMMENDATION_WATER_CHARGE_SCALE_RATE),
                ('wifi_charge', settings.RECOMMENDATION_WIFI_CHARGE_SCALE_RATE),
                ('rubbish_charge', settings.RECOMMENDATION_RUBBISH_CHARGE_SCALE_RATE),
                ('distance_value', settings.RECOMMENDATION_DISTANCE_VALUE_SCALE_RATE)
            ]
            for column, scale_rate in scaled_columns_and_rate:
                df[column] = self._min_max_scaler_with_rate(df[column].tolist(), scale_rate)

        return df
    
    def _normalize_rental_rooms_df(self, df: pd.DataFrame):
        normalized_df = normalize(df.values, norm='l2')
        return pd.DataFrame(normalized_df, index=df.index, columns=df.columns)
    
    def _get_top_k_closest_rooms(self, room_id: str, room_df: pd.DataFrame):
        k = settings.RECOMMENDATION_K_CLOSEST_ROOMS
        
        this_room = room_df['room_id' == room_id]
        for room in room_df['room_id' != room_id]:
            pass
    
    def get(self, request, renter):    
        weights = self._get_weights_of_searched_data(renter)
        if len(weights) == 0:
            return Response([], status=status.HTTP_200_OK)
        
        rental_rooms_df = self._get_scaled_rental_rooms_df(renter)
        if len(rental_rooms_df) == 0:
            return Response([], status=status.HTTP_200_OK)
        
        rental_rooms_df = self._normalize_rental_rooms_df(rental_rooms_df)
        
        
        recommendations = []

        return Response(recommendations, status=status.HTTP_200_OK)