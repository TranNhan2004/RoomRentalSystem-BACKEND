from rest_framework import viewsets

from .models import CustomUser, Lessor, Renter, Manager
from .serializers import CustomUserSerializer, LessorSerializer, RenterSerializer, ManagerSerializer


# -----------------------------------------------------------
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    
# -----------------------------------------------------------
class LessorViewSet(viewsets.ModelViewSet):
    queryset = Lessor.objects.all()
    serializer_class = LessorSerializer
    
    def get_object(self):
        user_id = self.kwargs.get("pk")
        return Lessor.objects.get(user__id=user_id)

    
# -----------------------------------------------------------
class RenterViewSet(viewsets.ModelViewSet):
    queryset = Renter.objects.all()
    serializer_class = RenterSerializer

    def get_object(self):
        user_id = self.kwargs.get("pk")
        return Renter.objects.get(user__id=user_id)

        
# -----------------------------------------------------------
class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def get_object(self):
        user_id = self.kwargs.get("pk")
        return Manager.objects.get(user__id=user_id)