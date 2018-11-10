from django.urls import path
from .views import login, logout, TodoGroupViewSet, TodoGroupMembersView, FriendsViewSet, register
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()

router.register('groups', TodoGroupViewSet, base_name='todo-group')
router.register('friends', FriendsViewSet, base_name='friend-requests')

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('register/', register),
    path('groups/<int:pk>/members/', TodoGroupMembersView.as_view()),
] + router.urls
