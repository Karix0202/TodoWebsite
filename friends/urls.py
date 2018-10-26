from django.urls import path
from .views import SendFriendRequestView, add_friend, index, accept, cancel_request
from django.contrib.auth.decorators import login_required

app_name = 'friends'

urlpatterns = [
    path('find/', login_required(SendFriendRequestView.as_view()), name='find'),
    path('send/<int:id>/', add_friend, name='add'),
    path('', index, name='index'),
    path('accept/<int:id>/', accept, name='accept'),
    path('delete/<int:id>/', cancel_request, name='delete'),
]
