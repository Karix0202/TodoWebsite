from rest_framework import serializers
from userauth.models import User
from friends.models import FriendRequest
from django.db.models import Q
from todo.models import TodoGroup


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('pk', 'username', 'profile_image', 'password', 'email', 'password2')

    def validate(self, data):
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError('User with this username already exists')
        
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError('Passwords are not same')

        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError('User with this email already exists')

        return data

    def create(self, validated_data):
        user = User()

        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        user.profile_image = validated_data['profile_image']
        user.email = validated_data['email']

        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'profile_image',)


class CreateOrUpdateFriendRequest(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('pk', 'sender', 'receiver', 'accepted')

    def validate(self, data):
        if 'sender' in data and 'receiver' in data:
            sender = data.get('sender')
            receiver = data.get('receiver')

            if receiver.pk is sender.pk:
                raise serializers.ValidationError('You can not send friends request to yourself')

            friend_req = FriendRequest.objects.filter(
                (Q(receiver=receiver) & Q(sender=sender)) |
                Q(receiver=sender) & Q(sender=receiver)
            ).first()

            if friend_req is not None:
                raise serializers.ValidationError('Friend request already exists')

        return data

    def create(self, validated_data):
        friend_request = FriendRequest()

        friend_request.receiver = validated_data['receiver']
        friend_request.sender = validated_data['sender']

        friend_request.save()

        return friend_request

    def update(self, instance, validated_data):
        instance.accepted = validated_data['accepted']
        instance.save()

        return instance


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ('pk', 'sender', 'receiver', 'accepted')


class CreateOrUpdateTodoGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoGroup
        fields = ('pk', 'name', 'photo', 'members', 'creator')

    def validate(self, data):
        if data.get('creator'):
            for member in data.get('members'):
                if member.pk is data.get('creator').pk:
                    continue
                if member not in data.get('creator').friends.all():
                    raise serializers.ValidationError('You cannot create group with users who are not your friends')

        return data

    def create(self, validated_data):
        group = TodoGroup()
        group.name = validated_data['name']
        group.photo = validated_data['photo']
        group.creator = validated_data['creator']

        group.save()

        for user in validated_data['members']:
            group.members.add(user)
        group.save()

        return group

    def update(self, instance, validated_data):
        if 'photo' in validated_data or 'name' in validated_data:
            if 'photo' in validated_data:
                instance.photo = validated_data['photo']

            if 'name' in validated_data:
                instance.name = validated_data['name']

            instance.save()

        return instance


class TodoGroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = TodoGroup
        fields = ('pk', 'name', 'photo', 'members', 'creator')


class RetrieveTodoGroupMembersSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = TodoGroup
        fields = ('members',)


class AddMembersToTodoGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoGroup
        fields = ('members',)

    def update(self, instance, validated_data):
        for new_member in validated_data['members']:
            print(new_member)
            instance.members.add(new_member)

        instance.save()

        return instance
