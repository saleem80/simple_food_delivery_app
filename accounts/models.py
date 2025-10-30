from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, mobile_number, **extra_fields):
        if not mobile_number:
            raise ValueError('The Mobile Number field must be set')
        
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_unusable_password()  # We use OTP authentication
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(mobile_number, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('delivery_partner', 'Delivery Partner'),
        ('admin', 'Admin'),
    ]
    
    mobile_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Additional fields for delivery partners
    is_available = models.BooleanField(default=True)  # For delivery partners
    
    objects = UserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.mobile_number} ({self.get_user_type_display()})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name


class OTPVerification(models.Model):
    mobile_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"OTP for {self.mobile_number}"
    
    def is_expired(self):
        # OTP expires after 10 minutes
        return (timezone.now() - self.created_at).seconds > 600
