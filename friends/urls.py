from django.urls import path
from .views import AddFriendView
from django.contrib.auth.decorators import login_required

app_name = 'friends'

urlpatterns = [
    path('add/', login_required(AddFriendView.as_view()), name='add')
]
