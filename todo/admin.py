from django.contrib import admin
from .models import TodoGroup, Todo

@admin.register(TodoGroup)
class TodoGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    pass