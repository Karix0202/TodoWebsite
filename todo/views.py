from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import CreateTodoGroupForm
from friends.models import FriendRequest
from django.db.models import Q

class CreateTodoGroupView(View):
    def get(self, request):
        form = CreateTodoGroupForm()
        friends = self.get_friends(request)
        return render(request, 'create.html', {'form': form, 'friends': friends})

    def post(self, request):
        form = CreateTodoGroupForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=True)

            return redirect(reverse('home:index'))
        
        return render(request, 'create.html', {'form': form, 'errors': form.errors})

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