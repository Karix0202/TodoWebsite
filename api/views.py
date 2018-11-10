from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ViewSet
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_201_CREATED
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.db.models import Q
from django.shortcuts import get_object_or_404
from friends.models import FriendRequest
from userauth.models import User
from todo.models import TodoGroup
from .serializers import UserSerializer, FriendRequestSerializer, TodoGroupSerializer, \
    CreateOrUpdateTodoGroupSerializer, RetrieveTodoGroupMembersSerializer, AddMembersToTodoGroupSerializer, \
    CreateOrUpdateFriendRequest


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
@api_view(['POST'])
def logout(request):
    token = Token.objects.filter(user=request.user).first()
    token.delete()

    Token.objects.create(user=request.user)
    logout(request._request)

    return Response({'message': 'Successfully logged out'}, status=HTTP_200_OK)


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
@api_view(['GET'])
def search_for_friends(request, username=None):
    user = request.user

    queryset = User.objects.filter(Q(username__icontains=username)).exclude(pk=user.pk).exclude(
        id__in=[u.pk for u in user.friends.all()])
    serializer = UserSerializer(queryset, many=True)

    return Response(serializer.data)


class FriendsViewSet(ViewSet):
    def list(self, request):
        queryset = FriendRequest.objects.filter(Q(receiver=request.user) | Q(sender=request.user))

        friends = queryset.filter(accepted=True)
        received = queryset.filter(receiver=request.user).exclude(accepted=True)
        sent = queryset.filter(sender=request.user).exclude(accepted=True)

        context = {
            'friends': UserSerializer(User.objects.filter(
                id__in=[req.receiver if req.sender.pk is request.user.pk else req.sender.id for req in friends]),
                                      many=True).data,
            'sent': UserSerializer(User.objects.filter(id__in=[req.receiver.pk for req in sent]), many=True).data,
            'received': UserSerializer(User.objects.filter(id__in=[u.sender.pk for u in received]), many=True).data
        }

        return Response(context)

    def create(self, request):
        serializer = CreateOrUpdateFriendRequest(data=request.data)

        if serializer.is_valid():
            serializer.save()
            retrieve_serializer = FriendRequestSerializer(FriendRequest.objects.get(pk=serializer.data.get('pk')))
            return Response(retrieve_serializer.data)

        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        friend_request = get_object_or_404(FriendRequest, pk=pk)
        user_id = request.user.pk

        if user_id is not friend_request.receiver.pk and user_id is not friend_request.sender.pk:
            return Response({
                'message': 'You can not accept others\' friend requests'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

        if friend_request.accepted:
            return Response({
                'message': 'Friend request is already accepted'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = CreateOrUpdateFriendRequest(friend_request, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            retrieve_serializer = FriendRequestSerializer(FriendRequest.objects.get(pk=serializer.data.get('pk')))
            return Response(retrieve_serializer.data)

        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        friend_request = get_object_or_404(FriendRequest, pk=pk)

        if friend_request.receiver.pk is not request.user.pk and friend_request.sender.pk is not request.user.pk:
            return Response({
                'message': 'You can not delete others\' friend requests'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

        friend_request.delete()

        return Response({'message': 'Success'})


class TodoGroupViewSet(ViewSet):
    def list(self, request):
        queryset = TodoGroup.objects.filter(members__id=request.user.id)
        serializer = TodoGroupSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TodoGroup.objects.all()

        todo_group = get_object_or_404(queryset, pk=pk)

        if todo_group not in queryset.filter(members__id=request.user.pk):
            return Response({'message': 'You can not get data from groups that you do not belong to'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = TodoGroupSerializer(todo_group)

        return Response(serializer.data)

    def create(self, request):
        serializer = CreateOrUpdateTodoGroupSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            queryset = TodoGroup.objects.get(pk=serializer.data.get('pk'))
            retrieve_serializer = TodoGroupSerializer(queryset)

            return Response(retrieve_serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        group = get_object_or_404(TodoGroup, pk=pk)

        if group.creator.pk is not request.user.pk:
            return Response({'message': 'You can not delete others group'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        group.delete()

        return Response({'message': 'success'}, status=HTTP_200_OK)

    def partial_update(self, request, pk=None):
        queryset = get_object_or_404(TodoGroup, pk=pk)

        if queryset.creator.pk is not request.user.pk:
            return Response({'message': 'You can not change information about group in which you are not creator'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = CreateOrUpdateTodoGroupSerializer(queryset, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            retrieve_serializer = TodoGroupSerializer(queryset)

            return Response(retrieve_serializer.data)

        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)


class TodoGroupMembersView(APIView):
    def get(self, request, pk=None):
        group = get_object_or_404(TodoGroup, pk=pk)

        if request.user not in group.members.all():
            return Response({'message': 'You can not get members of group that you do not belong to'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = RetrieveTodoGroupMembersSerializer(group)

        return Response(serializer.data)

    def patch(self, request, pk=None):
        group = get_object_or_404(TodoGroup, pk=pk)

        if request.user.pk is not group.creator.pk:
            return Response({'message': 'You can not add new user to the group if you are not creator of it'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        members = User.objects.filter(id__in=request.data.get('members'))

        for member in members:
            if member not in request.user.friends.all() and member.pk is not request.user.pk:
                return Response({'message': 'You can not add to group users which are not your friends'},
                                status=HTTP_500_INTERNAL_SERVER_ERROR)
            if member in group.members.all():
                return Response({'message': f'User with username: {member.username} is already member of this group'},
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = AddMembersToTodoGroupSerializer(instance=group, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(RetrieveTodoGroupMembersSerializer(group).data)

        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None):
        group = get_object_or_404(TodoGroup, pk=pk)

        if request.user not in group.members.all():
            return Response({'message': 'You can not get members of group that you do not belong to'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        if group.creator.pk is not request.user.pk:
            return Response({'message': 'You can not remove user from group that you are not creator'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        member = get_object_or_404(User, pk=request.data.get('user'))

        if member not in group.members.all():
            return Response({'message': 'User is not member of this group'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        if member.pk is request.user.pk:
            return Response({'message': 'You can not remove yourself from group if you are creator of it'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        group.members.remove(member)
        group.save()

        serializer = RetrieveTodoGroupMembersSerializer(group)

        return Response(serializer.data)
