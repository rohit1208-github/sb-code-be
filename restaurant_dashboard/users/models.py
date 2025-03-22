# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from management.models import Country, Branch

class UserRole(models.Model):
    LEADERSHIP = 'leadership'
    COUNTRY_LEADERSHIP = 'country_leadership'
    COUNTRY_ADMIN = 'country_admin'
    BRANCH_MANAGER = 'branch_manager'
    
    ROLE_CHOICES = [
        (LEADERSHIP, 'SB Leadership Team'),
        (COUNTRY_LEADERSHIP, 'Country Leadership Team'),
        (COUNTRY_ADMIN, 'Country Admin Team'),
        (BRANCH_MANAGER, 'Branch Manager'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.get_name_display()

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email