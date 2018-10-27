from django.contrib import admin
from .models import TodoGroup

@admin.register(TodoGroup)
class TodoGroupAdmin(admin.ModelAdmin):
    pass