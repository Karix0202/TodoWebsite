from django.urls import path
from .views import SendFriendRequestView, add_friend, index
from django.contrib.auth.decorators import login_required

app_name = 'friends'

urlpatterns = [
    path('find/', login_required(SendFriendRequestView.as_view()), name='find'),
    path('send/<int:id>/', add_friend, name='add'),
    path('', index, name='index')
]
