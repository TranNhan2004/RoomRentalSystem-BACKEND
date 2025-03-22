from django.urls import path
from .views import GetRecommendationsView


urlpatterns = [
    path('get-recommendations/', GetRecommendationsView.as_view(), name='get-recommendation')
]