from django.shortcuts import render
from django.views import View
from .forms import AddFriendForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import User

class AddFriendView(View):
    def get(self, request):
        form = AddFriendForm()
        return render(request, 'add_friend.html', {'form': form})

    def post(self, request):
        if not request.POST.get('username'):
            return HttpResponse(status=500)

        users = self.get_user_by_his_username(request.POST.get('username'), request)
        print(users)

        return JsonResponse({
            'username': request.POST.get('username')
        })

    def get_user_by_his_username(self, username, request):
        return User.objects.all().filter(
            Q(username__icontains=username)
        ).exclude(username=request.user.username)
        