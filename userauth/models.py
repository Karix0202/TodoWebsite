from django.db import models
from django.contrib.auth.models import AbstractUser as UserBase
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
import uuid

def get_profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile_images/', filename)

class User(UserBase):
    profile_image = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True)
    
    def __str__(self):
        return self.email

@receiver(post_delete, sender=User)
def _post_delete_receiver(sender, instance, **kwargs):
    if sender is User:
        storage, path = instance.profile_image.storage, instance.profile_image.path
        storage.delete(path)
    
