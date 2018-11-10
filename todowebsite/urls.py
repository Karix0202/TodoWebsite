from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('userauth.urls', namespace='userauth')),
    path('home/', include('home.urls', namespace='home')),
    path('home/friends/', include('friends.urls', namespace='friends')),
    path('home/todo/', include('todo.urls', namespace='todo')),
    path('api/', include('api.urls', namespace='api')),
    path('', index)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
