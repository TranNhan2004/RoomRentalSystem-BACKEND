from django.urls import path, include
from rest_framework import routers
from .views import GetRecommendationsView


urlpatterns = [
    path('get-recommendations/', GetRecommendationsView.as_view(), name='get-recommendation')
]