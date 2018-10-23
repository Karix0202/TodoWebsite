from django.shortcuts import render
from django.views.generic import View
from .forms import UserCreationForm

class LoginView(View):
    template = 'login.html'

    def get(self, request):
        return render(request, self.template, {})

    def post(self, request):
        pass

class RegisterView(View):
    template = 'register.html'

    def get(self, request):
        form = UserCreationForm(request.POST or None, request.GET or None)
        return render(request, self.template, {'form': form})

    def post(self, request):
        pass