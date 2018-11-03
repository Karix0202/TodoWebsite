from django.urls import path
from .views import FriendRequestView, login, logout

app_name = 'api'


urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('friend/', FriendRequestView.as_view()),
]
