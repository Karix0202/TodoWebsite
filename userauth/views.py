from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

class LoginView(View):
    template = 'login.html'

    def get(self, request):
        form = AuthenticationForm(request.POST or None)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST or None)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home:url')
        return render(request, self.template, {'form': form, 'errors': form.errors})

class RegisterView(View):
    template = 'register.html'

    def get(self, request):
        form = UserCreationForm(request.POST or None, request.GET or None)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.clean_password2
            user = authenticate(username=username, password=password)

            return render(request, 'success_register.html', {})

        return render(request, self.template, {'form': form, 'errors': form.errors})

def logout_user(request):
    logout(request)
    return redirect('/')
