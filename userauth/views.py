from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import UserCreationForm, AuthenticationForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

class LoginView(View):
    template = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(reverse('home:index'))
        
        return render(request, self.template, {'form': form, 'errors': form.errors})

class RegisterView(View):
    template = 'register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.clean_password2
            user = authenticate(username=username, password=password)

            return render(request, 'success_register.html', {})

        return render(request, self.template, {'form': form, 'errors': form.errors})

def logout_user(request):
    logout(request)
    return redirect(reverse('userauth:login'))
