from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


# -----------------------------------------------------------
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    

# -----------------------------------------------------------
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            response.set_cookie(
                'refresh_token',  
                refresh_token,   
                max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),  
                expires=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),  
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],      
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTPONLY'],   
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                domain='.localhost',
                   
            )
            
            # print(int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()))
            # print(int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()))
            # print(settings.SIMPLE_JWT['AUTH_COOKIE_PATH'])
            # print(settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'])
            # print(settings.SIMPLE_JWT['AUTH_COOKIE_HTTPONLY'])
            # print(settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'])
            response.data.pop('refresh')
        return response


# -----------------------------------------------------------
class CheckLoginStatusView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'code': 'authenticated'}, status=status.HTTP_200_OK)


# -----------------------------------------------------------
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        print(refresh_token)
        
        if not refresh_token:
            return Response({'detail': 'Refresh token missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            return Response({'access': str(access_token)}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': 'Invalid or expired refresh token'}, status=status.HTTP_400_BAD_REQUEST)

    
# -----------------------------------------------------------
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token', path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']) 
        return response