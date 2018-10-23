from django.db import models
from django.contrib.auth.models import AbstractUser as UserBase

class User(UserBase):
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.email