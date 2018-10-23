from django.urls import path
from .views import LoginView, RegisterView, logout_user

app_name = 'userauth'

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_user, name='logout')
]