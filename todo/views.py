from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .forms import CreateTodoGroupForm, TodoForm
from friends.models import FriendRequest
from .models import TodoGroup
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

class CreateTodoGroupView(View):
    def get(self, request):
        form = CreateTodoGroupForm()
        form.fields['members'].queryset = request.user.friends.all()

        return render(request, 'todo/create.html', {'form': form})

    def post(self, request):
        form = CreateTodoGroupForm(request.POST, request.FILES)
        form.fields['members'].queryset = request.user.friends.all()

        if form.is_valid():
            group = form.save()
            group.members.add(request.user)
            group.save()

            return redirect(group.get_absolute_url())
        
        return render(request, 'todo/create.html', {'form': form, 'errors': form.errors})

@login_required
def index(request):
    groups = TodoGroup.objects.filter(members__id=request.user.id).all()
    
    return render(request, 'todo/index.html', {'groups': groups})

@login_required
def group(request, slug):
    group = TodoGroup.objects.filter(slug=slug).first()
    ff = TodoForm(request=request)

    if group is None:
        return HttpResponse(status=404)

    return render(request, 'todo/group.html', {'group': group})