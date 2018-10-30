from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import CreateTodoGroupView, index, GroupView, change_state

app_name = 'todo'

urlpatterns = [
    path('create/', login_required(CreateTodoGroupView.as_view()), name='create'),
    path('', index, name='list'),
    path('group/<slug:slug>/', login_required(GroupView.as_view()), name='single_group'),
    path('change/<int:id>/', change_state, name='change_state'),
]