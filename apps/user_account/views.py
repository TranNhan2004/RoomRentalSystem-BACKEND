from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend_project.choices import ROLE_CHOICES
from backend_project.email_bodies import (
    get_activate_account_email_body,
    get_reset_password_email_body
)

from services.user_account import update_coords_and_distances_for_renter

from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from .filters import CustomUserFilter


# -----------------------------------------------------------
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filterset_class = CustomUserFilter
    
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        request.data.pop('id', None)
        request.data.pop('password', None)
        request.data.pop('created_at', None)
        request.data.pop('updated_at', None)
        request.data.pop('last_login', None)
        return super().partial_update(request, *args, **kwargs)

    
# -----------------------------------------------------------
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        refresh = response.data.get('refresh')
        user_role = response.data.get('user', {}).get('role')
        
        if refresh and user_role:
            response.set_cookie(
                key=settings.SESSION_REFRESH_TOKEN_COOKIE_KEYS[user_role],
                value=refresh,
                max_age=settings.SESSION_REFRESH_TOKEN_COOKIE_MAX_AGE,
                secure=True,
                httponly=True,
                samesite='None',
                domain=settings.SESSION_REFRESH_TOKEN_COOKIE_DOMAIN,
                path=settings.SESSION_REFRESH_TOKEN_COOKIE_PATH
            )
        
            response.data.pop('refresh', None)
            return response
        
        return Response({"detail": "Invalid refresh token or user role"}, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    
    def post(self, request, *args, **kwargs):
        user_role = request.data.get('role')
        if user_role not in [role[0] for role in ROLE_CHOICES]:
            return Response({"detail": "Invalid user role"}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh_token = request.COOKIES.get(settings.SESSION_REFRESH_TOKEN_COOKIE_KEYS[user_role])

        if not refresh_token:
            return Response({"detail": "Refresh token is missing."}, status=status.HTTP_400_BAD_REQUEST)
            
        request.data['refresh'] = refresh_token
        return super().post(request, *args, **kwargs)


# -----------------------------------------------------------
class SendEmailForResetPasswordView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        user_email = request.data.get('email')
        
        try:
            user = get_user_model().objects.get(email=user_email)
        except get_user_model().DoesNotExist:
            return Response({"detail": "Email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        uidb64 = urlsafe_base64_encode(str(user.id).encode())
        token = default_token_generator.make_token(user)
                
        reset_link = request.build_absolute_uri(reverse(
            viewname='auth-reset-password-confirm', 
            kwargs={'uidb64': uidb64, 'token': token}
        ))
        reset_link = reset_link.replace(
            settings.BACKEND_URL_FOR_SEND_EMAIL,
            settings.FRONTEND_URLS_FOR_SEND_EMAIL[user.role]
        ) 

        try:
            email = EmailMessage(
                subject='ĐẶT LẠI MẬT KHẨU',
                body=get_reset_password_email_body(reset_link),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.content_subtype = 'html'
            email.send()
        except Exception as e:
            return Response({"detail": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "Your link to reset password has been sent"}, status=status.HTTP_200_OK)


# -----------------------------------------------------------
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(id=uid)
        except (ValueError, get_user_model().DoesNotExist):
            return Response({"detail": "Token is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Token is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')
        
        if new_password != confirm_new_password:
            return Response(
                {"detail": "Confirm new password does not match with new password"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been reset successfully"}, status=status.HTTP_200_OK)
    

# -----------------------------------------------------------
class ChangePasswordView(APIView):
    def patch(self, request, id):
        try:
            user = get_user_model().objects.get(id=id)
        except get_user_model().DoesNotExist:
            return Response({"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_new_password:
            return Response(
                {"detail": "Confirm new password does not match with new password"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if old_password == new_password:
            return Response(
                {"detail": "Old password and new password cannot be the same"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been changed successfully"}, status=status.HTTP_200_OK)


# -----------------------------------------------------------
class SendEmailForRegisterView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        data = request.data.copy()  
        data['is_active'] = False  
        
        if data.get('password') != data.get('confirm_password'):
            return Response(
                {"detail": "Confirm new password does not match with new password"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CustomUserSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        
        uidb64 = urlsafe_base64_encode(str(user.id).encode())
        token = default_token_generator.make_token(user)
        
        activate_link = request.build_absolute_uri(reverse(
            viewname='auth-activate-account', 
            kwargs={'uidb64': uidb64, 'token': token}
        ))
        
        activate_link = activate_link.replace(
            settings.BACKEND_URL_FOR_SEND_EMAIL,
            settings.FRONTEND_URLS_FOR_SEND_EMAIL[user.role]
        )
        
        print(activate_link)

        try:
            email = EmailMessage(
                subject='KÍCH HOẠT TÀI KHOẢN',
                body=get_activate_account_email_body(activate_link),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.content_subtype = 'html'
            email.send()
        except Exception as e:
            return Response({"detail": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "Your link to activate account has been sent"}, status=status.HTTP_200_OK)


# -----------------------------------------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(id=uid)
        except (ValueError, get_user_model().DoesNotExist):
            return Response({"detail": "Token is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Token is not valid or expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_active:
            return Response({"detail": "Your account is already activated"}, status=status.HTTP_200_OK)

        user.is_active = True
        user.save()
        
        if user.role == 'RENTER':
            update_coords_and_distances_for_renter(user.id, user.workplace_commune.id, user.workplace_additional_address)

        return Response({"detail": "Your account has been activated successfully"}, status=status.HTTP_200_OK)