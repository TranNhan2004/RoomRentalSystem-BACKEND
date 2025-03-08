import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from backend_project.choices import GENDER_CHOICES, ROLE_CHOICES
from apps.address.models import Commune


# -----------------------------------------------------------
# For admin
class CustomUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        return self.create_user(email, email, password, **extra_fields)
    
    
# -----------------------------------------------------------
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=128, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128)
    citizen_number = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='MALE')
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='RENTER')
    
    # For role == 'R'
    workplace_commune = models.ForeignKey(
        Commune, 
        related_name='working_renters', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True
    )
    workplace_additional_address = models.TextField(max_length=512, null=True, blank=True)
    workplace_latitude = models.FloatField(null=True, blank=True)
    workplace_longitude = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.username = self.email

        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email