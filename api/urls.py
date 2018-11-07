from django.urls import path
from .views import FriendRequestView, login, logout, TodoGroupViewSet, TodoGroupMembersView
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()

router.register('groups', TodoGroupViewSet, base_name='todo-group')

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('friend/', FriendRequestView.as_view()),
    path('groups/<int:pk>/members/', TodoGroupMembersView.as_view()),
] + router.urls
