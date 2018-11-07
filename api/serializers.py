from rest_framework import serializers
from userauth.models import User
from friends.models import FriendRequest
from django.db.models import Q
from todo.models import TodoGroup


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'profile_image',)


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('pk', 'sender', 'receiver', 'accepted')

    def validate(self, data):

        if data.get('sender') and data.get('sender'):
            sender = data.get('sender')
            receiver = data.get('receiver')

            if receiver is None:
                raise serializers.ValidationError('User does not exists')

            if sender.pk == receiver.pk:
                raise serializers.ValidationError('You can not send friend request to yourself')

            queryset = FriendRequest.objects.filter(
                (Q(sender=sender) & Q(receiver=receiver)) |
                (Q(sender=receiver) & Q(receiver=sender))
            )

            if len(queryset) > 0:
                raise serializers.ValidationError('You have alredy send a friend request to this user')

        if 'accepted' in data:
            if data.get('accepted') is False:
                raise serializers.ValidationError('Wrong accept value')

        return data

    def create(self, validated_data):
        return FriendRequest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.accepted = validated_data['accepted']
        instance.save()

        return instance


class CreateOrUpdateTodoGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoGroup
        fields = ('pk', 'name', 'photo', 'members', 'creator')

    def validate(self, data):
        if data.get('creator'):
            for member in data.get('members'):
                if member.pk is data.get('creator').pk:
                    continue
                if not member in data.get('creator').friends.all():
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
