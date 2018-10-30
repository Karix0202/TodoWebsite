from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .forms import CreateTodoGroupForm, AddTodoForm
from friends.models import FriendRequest
from .models import TodoGroup, Todo
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

class GroupView(View):
    def get(self, request, slug):
        group = TodoGroup.objects.filter(slug=slug).first()

        if group is None:
            return HttpResponse(status=404)

        if not request.user in group.members.all():
            return redirect(reverse('home:index'))

        form = AddTodoForm()
        form.fields['user'].queryset = group.members.all()

        return render(request, 'todo/group.html', {'group': group, 'form': form, 'todos': self.get_all_todos(group)})

    def post(self, request, slug):
        group = TodoGroup.objects.filter(slug=slug).first()
        
        if group is None:
            return HttpResponse(status=404)

        if not request.user in group.members.all():
            return redirect(reverse('home:index'))

        form = AddTodoForm(request.POST)
        form.fields['user'].queryset = group.members.all()

        context = {'group': group, 'form': form, 'todos': self.get_all_todos(group)}

        if form.is_valid():
            form.save()
            return redirect(group.get_absolute_url())

        context['errors'] = forms.errors
        return render(request, 'todo/group.html', context)

    
    def get_all_todos(self, group):
        return Todo.objects.filter(Q(group=group)).all()
    
@login_required
def change_state(request, id):
    todo = get_object_or_404(Todo, pk=id)

    if todo.user != request.user:
        return HttpResponse(status=404)

    todo.done = False if todo.done else True;
    todo.save()

    return redirect(todo.group.get_absolute_url())
