from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    # is_verified = models.BooleanField(default=False)  # This would be changed through email token verification
    type = models.CharField(max_length=10, 
                            choices=[("admin", "Admin"), ("customer", "Customer")], 
                            default="customer")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()} | {self.email}" 