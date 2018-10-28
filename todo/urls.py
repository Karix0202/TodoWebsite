from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import CreateTodoGroupView, index, group

app_name = 'todo'

urlpatterns = [
    path('create/', login_required(CreateTodoGroupView.as_view()), name='create'),
    path('', index, name='list'),
    path('group/<slug:slug>/', group, name='single_group')
]