from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from .forms import AddFriendForm
from django.http import HttpResponse, JsonResponse, Http404
from django.db.models import Q
from userauth.models import User
from .models import FriendRequest
from django.contrib.auth.decorators import login_required

class SendFriendRequestView(View):
    def get(self, request):
        form = AddFriendForm()
        return render(request, 'add_friend.html', {'form': form})

    def post(self, request):
        form = AddFriendForm(request.POST)

        ctx = {'form': form}

        if form.is_valid():
            username = form.cleaned_data['username']
            users = self.get_users(request, username)
            ctx['users'] = users

        return render(request, 'add_friend.html', ctx)

    def get_user_by_his_username(self, request, username):
        return User.objects.filter(
            Q(username__icontains=username)
        ).exclude(username=request.user.username)
        
    def are_users_friends(self, request, user):
        sended = FriendRequest.objects.filter(sender=request.user).filter(receiver=user)
        received = FriendRequest.objects.filter(sender=request.user).filter(receiver=request.user)
        return True if len(sended) > 0 or len(received) > 0 else False

    def get_proper_users(self, request, username):
        users = self.get_user_by_his_username(request, username)
        for user in users:
            if not self.are_users_friends(request, user):
                yield {
                    'username': user.username,
                    'id': user.id,
                    'profile_image': user.profile_image.url
                }

    def get_users(self, request, username):
        return [user for user in self.get_proper_users(request, username)]

@login_required
def add_friend(request, id):
    if request.user.id == id:
        return HttpResponse('its you')

    receiver = User.objects.filter(id=id).first()

    if FriendRequest.objects.filter(receiver=receiver).filter(sender=request.user).first() is not None or FriendRequest.objects.filter(sender=receiver).filter(receiver=request.user).first() is not None:
        return HttpResponse(status=500)

    friend_request = FriendRequest(receiver=receiver, sender=request.user)
    friend_request.save()

    return redirect(reverse('friends:find'))

@login_required
def index(request):
    waiting_for_accept = FriendRequest.objects.filter(receiver=request.user).filter(accepted=False)
    sended = FriendRequest.objects.filter(sender=request.user).filter(accepted=False)
    friends = FriendRequest.objects.filter(
        Q(receiver=request.user) |
        Q(sender=request.user)
    ).filter(accepted=True)

    return render(request, 'list.html', {
        'waiting_for_accept': waiting_for_accept,
        'sended': sended,
        'friends': friends,
    })

@login_required
def cancel_request(request, id):
    req = get_object_or_404(FriendRequest, pk=id)
    req.delete()
    return redirect(reverse('friends:index'))

@login_required
def accept(request, id):
    friend_request = get_object_or_404(FriendRequest, pk=id)

    if friend_request.receiver != request.user:
        return HttpResponse(status=404)

    friend_request.accepted = True
    friend_request.save()

    return redirect(reverse('friends:index'))