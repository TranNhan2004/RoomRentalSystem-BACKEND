import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

from typing import List, Dict

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.rental_room.models import RentalRoom, Charges
from apps.search_room_history.models import SearchRoomHistory
from apps.distance.models import Distance

from backend_project.utils import today
from backend_project.permissions import IsRenter

# -----------------------------------------------------------
class GetRecommendationsView(APIView):
    permission_classes = [IsAuthenticated, IsRenter]
    
    def _min_max_scaler_with_rate(self, data: List[float], scale_rate: float):
        data = np.array(data)
        old_min = np.min(data)
        old_max = np.max(data)

        if old_min == old_max:
            return np.full_like(data, fill_value=scale_rate, dtype=float)
        
        scaled_data = (data - old_min) / (old_max - old_min)
        scaled_data = scaled_data * scale_rate
        return scaled_data
    
    def _get_searched_data(self, renter_id: str) -> Dict[str, dict]:
        search_room_histories = SearchRoomHistory.objects.filter(renter=renter_id).order_by('-created_at')
        
        if not search_room_histories.exists():
            return {}
        
        max_date = search_room_histories.first().created_at.date()
        if max_date == today():
            return {}
        
        searched_data = {}
        for search_room_history in search_room_histories:
            room_id = search_room_history.rental_room.id
            if room_id not in searched_data:
                searched_data[room_id] = {
                    'weight': search_room_history.weight,
                    'created_at': search_room_history.created_at
                }
            else:
                searched_data[room_id]['weight'] += search_room_history.weight
        
        for room_id in searched_data:
            days_diff = (max_date - searched_data[room_id]['created_at'].date()).days + 1  
            searched_data[room_id]['weight'] *= (1 / days_diff)
        
        return searched_data
    
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
        if df.empty:
            return df

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
        feature_columns = ['room_charge', 'electricity_charge', 'water_charge',
                          'wifi_charge', 'rubbish_charge', 'distance_value']
        normalized_values = normalize(df[feature_columns].values, norm='l2')
        normalized_df = pd.DataFrame(normalized_values, index=df.index, columns=feature_columns)
        normalized_df['id'] = df['id']
        return normalized_df

    def _get_top_k_closest_rooms(self, room_id: str, rental_rooms_df: pd.DataFrame):
        k = settings.RECOMMENDATION_K_CLOSEST_ROOMS
        
        target_room = rental_rooms_df[rental_rooms_df['id'] == room_id]
        if target_room.empty:
            return []
        
        feature_columns = ['room_charge', 'electricity_charge', 'water_charge',
                          'wifi_charge', 'rubbish_charge', 'distance_value']
        target_vector = target_room[feature_columns].values
        all_vectors = rental_rooms_df[feature_columns].values
        
        similarities = cosine_similarity(target_vector, all_vectors)[0]
        
        rental_rooms_df['similarity_to_target'] = similarities
        
        closest_rooms = rental_rooms_df[rental_rooms_df['id'] != room_id] \
            .sort_values('similarity_to_target', ascending=False) \
            .head(k)
        
        return closest_rooms['id'].tolist()
    
    
    def get(self, request):
        renter = request.query_params.get('renter')
        if not renter:
            return Response({'data': 'Renter ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        searched_data = self._get_searched_data(renter)
        if not searched_data:
            return Response([], status=status.HTTP_200_OK)
        
        rental_rooms_df = self._get_scaled_rental_rooms_df(renter)
        if rental_rooms_df.empty:
            return Response([], status=status.HTTP_200_OK)
        
        normalized_df = self._normalize_rental_rooms_df(rental_rooms_df)
        rental_rooms_df[normalized_df.columns] = normalized_df
        
        recommendation_weights = {}
        for room_id, data in searched_data.items():
            k_closest_rooms = self._get_top_k_closest_rooms(room_id, rental_rooms_df)
            weight = data['weight']
            for closest_room_id in k_closest_rooms:
                recommendation_weights[closest_room_id] = \
                    recommendation_weights.get(closest_room_id, 0) + weight
        
        k = settings.RECOMMENDATION_K_CLOSEST_ROOMS
        recommendations = sorted(
            recommendation_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]
        
        recommendation_list = [{"rental_room": room_id} for room_id, _ in recommendations]
        
        return Response(recommendation_list, status=status.HTTP_200_OK)