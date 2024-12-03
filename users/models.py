from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    
    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone}"
