import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from backend_project.utils import upload_to_fn
from apps.address.models import Commune


# -----------------------------------------------------------
# For admin
class CustomUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'A')
        return self.create_user(email, email, password, **extra_fields)
    
    
# -----------------------------------------------------------
def user_avatar_upload_to(instance, filename):
    return upload_to_fn(
        folders_path=['avatars', f'user-{instance.id}'],
        filename=filename
    )
    
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=128, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128)
    citizen_number = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    GENDER_CHOICES = [
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('U', 'Không rõ')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    avatar = models.ImageField(upload_to=user_avatar_upload_to, null=True, blank=True)
    
    ROLE_CHOICES = [
        ('A', 'Quản trị viên'),
        ('M', 'Quản lý'),
        ('L', 'Người cho thuê'),
        ('R', 'Người thuê')
    ]
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    
    # For role == 'R'
    workplace_commune = models.ForeignKey(
        Commune, 
        related_name='working_renters', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    workplace_additional_address = models.TextField(max_length=512, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email

        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email