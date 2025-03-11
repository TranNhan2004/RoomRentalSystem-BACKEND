from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend_project.utils import equals_address
from backend_project.goong_api import get_coords, get_distance_value
from backend_project.email_bodies import (
    get_activate_account_email_body,
    get_reset_password_email_body
)

from apps.address.models import Province, District, Commune
from apps.rental_room.models import RentalRoom
from apps.distance.models import Distance

from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from .filters import CustomUserFilter


def update_coords_and_distances_for_renter(renter_id, workplace_commune_id, workplace_additional_address):
        commune = get_object_or_404(Commune, id=workplace_commune_id)
        district = get_object_or_404(District, id=commune.district.id)
        province = get_object_or_404(Province, id=district.province.id)
            
        renter_wokplace_coords = get_coords(
            f"{workplace_additional_address}, {commune.name}, {district.name}, {province.name}"
        )        
        
        renter = get_object_or_404(CustomUser, id=renter_id)
        renter.workplace_latitude = renter_wokplace_coords[0]
        renter.workplace_longitude = renter_wokplace_coords[1]
        renter.save()
        
        Distance.objects.filter(renter=renter.id).delete()
        rental_rooms = RentalRoom.objects.all()

        distances = []
        for rental_room in rental_rooms:
            room_coords = (rental_room.latitude, rental_room.longitude)
            value = get_distance_value(room_coords, renter_wokplace_coords)
            distances.append(Distance(renter=renter.id, rental_room=renter_id, value=value))

        Distance.objects.bulk_create(distances)

# -----------------------------------------------------------
class CustomUserViewSet(viewsets.ModelViewSet):
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
        
        instance = self.get_object()
        old_workplace_commune_id = instance.commune.id
        old_workplace_additional_address = instance.additional_address
        old_workplace_address = f"{old_workplace_additional_address}, {old_workplace_commune_id}"

        response = super().partial_update(request, *args, **kwargs)
        user_role = response.data.get('role')
        
        if user_role == 'RENTER':
            renter_id = response.data.get('id')

            new_workplace_commune_id = response.data.get('workplace_commune')
            new_workplace_additional_address = response.data.get('workplace_additional_address')
            new_workplace_address = f"{new_workplace_additional_address}, {new_workplace_commune_id}"

            if not equals_address(old_workplace_address, new_workplace_address):
                update_coords_and_distances_for_renter(renter_id, new_workplace_commune_id, new_workplace_address)

        return response

    
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

    def post(self, request, *args, **kwargs):
        user_email = request.data.get('email')
        
        try:
            user = get_user_model().objects.get(email=user_email)
        except get_user_model().DoesNotExist:
            return Response({"detail": "Email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        uidb64 = urlsafe_base64_encode(str(user.id).encode())
        token = default_token_generator.make_token(user)

        role_to_idx = {
            'MANAGER': 0,
            'LESSOR': 1,
            'RENTER': 2
        }
        if user.role not in role_to_idx:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

                
        reset_link = request.build_absolute_uri(reverse(
            viewname='auth-reset-password-confirm', 
            kwargs={'uidb64': uidb64, 'token': token}
        ))
        reset_link = reset_link.replace(
            settings.BACKEND_URL_FOR_SEND_EMAIL,
            settings.FRONTEND_URLS_REPLACE_FOR_SEND_EMAIL[role_to_idx[user.role]]
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
            return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        role_to_idx = {
            'LESSOR': 1, 
            'RENTER': 2
        }
        if user.role not in role_to_idx:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        
        activate_link = request.build_absolute_uri(reverse(
            viewname='auth-activate-account', 
            kwargs={'uidb64': uidb64, 'token': token}
        ))
        activate_link = activate_link.replace(
            settings.BACKEND_URL_FOR_SEND_EMAIL,
            settings.FRONTEND_URLS_REPLACE_FOR_SEND_EMAIL[role_to_idx[user.role]]
        )

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
            return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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