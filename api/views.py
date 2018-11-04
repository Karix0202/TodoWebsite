from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ViewSet
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.db.models import Q
from django.shortcuts import get_object_or_404
from friends.models import FriendRequest
from userauth.models import User
from todo.models import TodoGroup
from .serializers import UserSerializer, FriendRequestSerializer, TodoGroupSerializer


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


@permission_classes((IsAuthenticated))
@authentication_classes((TokenAuthentication))
@api_view(['POST'])
def logout(request):
    token = Token.objects.filter(user=request.user).first()
    token.delete()

    Token.objects.create(user=request.user)
    logout(request._request)

    return Response({'message': 'Successfully logged out'}, status=HTTP_200_OK)


class FriendRequestView(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        user = request.user

        queryset = User.objects.filter(Q(username__icontains=username)).exclude(pk=user.pk).exclude(
            id__in=[u.id for u in user.friends.all()])
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        pk = self.request.data['id']

        data = {
            'sender': request.user.pk,
            'receiver': pk
        }

        serializer = FriendRequestSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, requset):
        pk = self.request.data['id']

        user = requset.user
        second_user = get_object_or_404(User, pk=pk)

        friend_request = FriendRequest.objects.filter(
            (Q(sender=user) & Q(receiver=second_user)) |
            (Q(sender=second_user) & Q(receiver=user))
        ).first()

        if friend_request is None:
            return Response('Friend request not found', status=HTTP_404_NOT_FOUND)

        if friend_request.receiver.pk != user.pk == friend_request.sender.pk != user.pk:
            return Response('You are not one of the users from this friend request',
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        friend_request.delete()

        return Response(status=HTTP_200_OK)

    def patch(self, request):
        queryset = FriendRequest.objects.get(pk=request.data.get('id'))

        user_id = request.user.pk

        if user_id is not queryset.receiver.pk and user_id is not queryset.sender.pk:
            return Response({
                'non_field_errors': [
                    "You can not accept others' friend requests"
                ]
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

        if queryset.accepted:
            return Response({
                'non_field_errors': [
                    'Friend request is already accepted'
                ]
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = FriendRequestSerializer(queryset, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)


class TodoGroupViewSet(ViewSet):
    def list(self, request):
        queryset = TodoGroup.objects.filter(members__id=request.user.id)
        serializer = TodoGroupSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TodoGroup.objects.all()

        todo_group = get_object_or_404(queryset, pk=pk)

        if not todo_group in queryset.filter(members__id=request.user.pk):
            return Response({'message': 'You can not get data from groups that you do not belong to'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = TodoGroupSerializer(todo_group)

        return Response(serializer.data)

    def create(self, request):
        request.data['creator'] = request.user.pk
        serializer = TodoGroupSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)