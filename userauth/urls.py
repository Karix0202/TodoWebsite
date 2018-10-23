from django.urls import path
from .views import LoginView, RegisterView

app_name = 'userauth'

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
]