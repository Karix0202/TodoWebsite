from django.db import models
from userauth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.shortcuts import reverse
import uuid
import os

def get_group_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('group_photos/', filename)

class TodoGroup(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=get_group_photo_path)
    slug = models.SlugField(unique=True, blank=True)
    members = models.ManyToManyField(User)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('todo:single_group', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-created',)

@receiver(post_delete, sender=TodoGroup)
def _todo_group_post_delete(sender, instance, **kwargs):
    if sender is TodoGroup:
        storage, path = instance.photo.storage, instance.photo.path
        storage.delete(path)

def create_slug(instance, new_slug=None):
    slug = new_slug if new_slug is not None else slugify(instance.name)
    qs = TodoGroup.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s' % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

@receiver(pre_save, sender=TodoGroup)
def _post_save_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    

