from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class roles(models.Model):
    role_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.role_name

class address(models.Model):
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, default="N/A", blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.line_1}, {self.city}, {self.state}"

class user_accs(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('banned', 'Banned'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)  # Store hashed passwords
    role = models.ForeignKey(roles, on_delete=models.SET_DEFAULT, default=2)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.ForeignKey(address, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    # Required fields for Django Authentication
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)  # Needed for Django authentication
    is_staff = models.BooleanField(default=False)  # Needed for Django admin access
    USERNAME_FIELD = 'email'  # Email will be used as the unique identifier
    REQUIRED_FIELDS = ['name']  # Required fields for createsuperuser
    def __str__(self):
        return self.name
    
    def set_password(self, raw_password):
        """ Set the password by hashing it """
        self.password_hash = make_password(raw_password)

    def save(self, *args, **kwargs):
        # Ensure password is hashed before saving
        if not self.password_hash.startswith('pbkdf2_sha256$'):  
            self.password_hash = make_password(self.password_hash)
        super().save(*args, **kwargs)

class permission(models.Model):
    role = models.ForeignKey(roles, on_delete=models.CASCADE)
    permission_detail = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.role.role_name} - {self.permission_detail}"
