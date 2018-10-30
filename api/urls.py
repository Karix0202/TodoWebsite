from django.urls import path
from rest_framework.authtoken import views
from .views import TokenAuth

app_name = 'api'

urlpatterns = [
    path('login/', TokenAuth.as_view())
]