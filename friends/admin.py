from django.contrib import admin
from .models import FriendRequest

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    pass