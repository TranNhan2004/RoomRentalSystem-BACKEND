from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings


# -----------------------------------------------------------
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    

# -----------------------------------------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            response.set_cookie(
                'refresh_token',  
                refresh_token,   
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],  
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],  
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],      
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTPONLY'],   
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']   
            )
        response.data.pop('refresh')
        return response


# -----------------------------------------------------------
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    
    
# -----------------------------------------------------------
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token', path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']) 
        return response