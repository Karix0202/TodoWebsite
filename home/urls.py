from django.urls import path, include
from .views import index_view

app_name = 'home'

urlpatterns = [
    path('', index_view, name='index'),
    path('friends/', include('friends.urls', namespace='friends'))
]