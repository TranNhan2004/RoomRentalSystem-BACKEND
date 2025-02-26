from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer


# -----------------------------------------------------------
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        request.data.pop('password')
        return super().partial_update(request, *args, **kwargs)

    

# -----------------------------------------------------------
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        req_user_role = request.data.get('role')
        res_user_role = response.data.get('user').get('role')
        if response.status_code == 200 and req_user_role != res_user_role:
            return Response({'detail': 'Invalid role'}, status=status.HTTP_403_FORBIDDEN)
        
        res_user_id = response.data.get('user').get('id')
        user = get_user_model().objects.get(id=res_user_id)
        user.last_login = now()
        user.save()
        user.refresh_from_db()
        
        response.data['user'] = CustomUserSerializer(user).data     
        return response


# -----------------------------------------------------------
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


# -----------------------------------------------------------
class SendEmailForResetPasswordView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        user_email = request.data.get('email')
        
        try:
            user = get_user_model().objects.get(email=user_email)
        except get_user_model().DoesNotExist:
            return Response({"detail": "Email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        uidb64 = urlsafe_base64_encode(str(user.id).encode())
        token = default_token_generator.make_token(user)

        role_to_idx = {
            'M': 0,
            'L': 1,
            'R': 2
        }        
        reset_link = request.build_absolute_uri(reverse(
            viewname='auth-reset-password-confirm', 
            kwargs={'uidb64': uidb64, 'token': token}
        ))
        reset_link = reset_link.replace(
            settings.BACKEND_URL_FOR_SEND_EMAIL,
            settings.FRONTEND_URLS_REPLACE_FOR_SEND_EMAIL[role_to_idx[user.role]]
        ) 

        send_mail(
            subject='ĐẶT LẠI MẬT KHẨU',
            message=f'Vui lòng nhấp vào liên kết sau để đặt lại mật khẩu: \n{reset_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )

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
    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id')
            user = get_user_model().objects.get(id=id)
        except get_user_model().DoesNotExist:
            return Response({"detail": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

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
        
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been changed successfully"}, status=status.HTTP_200_OK)
