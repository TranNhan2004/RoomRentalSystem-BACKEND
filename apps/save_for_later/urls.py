from django.urls import path, include
from rest_framework import routers
from .views import SaveForLaterViewSet

router = routers.DefaultRouter()
router.register(r'save-for-later', SaveForLaterViewSet, basename='save-for-later')

urlpatterns = [
    path('', include(router.urls)),
]