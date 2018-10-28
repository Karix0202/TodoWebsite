from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .forms import CreateTodoGroupForm
from friends.models import FriendRequest
from .models import TodoGroup
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

class CreateTodoGroupView(View):
    def get(self, request):
        form = CreateTodoGroupForm()
        friends = self.get_friends(request)
        return render(request, 'todo/create.html', {'form': form, 'friends': friends})

    def post(self, request):
        form = CreateTodoGroupForm(request.POST, request.FILES)

        if form.is_valid():
            group = form.save()
            group.members.add(request.user)
            group.save()

            return redirect(reverse('todo:index'))
        
        return render(request, 'todo/create.html', {'form': form, 'errors': form.errors})

    def filter_friendships(self, request):
        friends = FriendRequest.objects.filter(
            Q(receiver=request.user) |
            Q(sender=request.user)
        ).filter(accepted=True)

        for friendship in friends:
            if friendship.receiver == request.user:
                yield friendship.sender
            else:
                yield friendship.receiver

    def get_friends(self, request):
        return [user for user in self.filter_friendships(request)]

@login_required
def index(request):
    groups = TodoGroup.objects.filter(members__id=request.user.id).all()
    
    return render(request, 'todo/index.html', {'groups': groups})

@login_required
def group(request, slug):
    group = TodoGroup.objects.filter(slug=slug).first()

    if group is None:
        return HttpResponse(status=404)

    return render(request, 'todo/group.html', {'group': group})