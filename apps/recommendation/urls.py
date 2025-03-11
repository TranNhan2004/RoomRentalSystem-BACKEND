from django.urls import path
from .views import GetRecommendationsView


urlpatterns = [
    path('get-recommendations/<str:renter>', GetRecommendationsView.as_view(), name='get-recommendation')
]