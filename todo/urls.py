from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import CreateTodoGroupView

app_name = 'todo'

urlpatterns = [
    path('create/', login_required(CreateTodoGroupView.as_view()), name='create')
]