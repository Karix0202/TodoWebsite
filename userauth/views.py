from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import UserCreationForm, AuthenticationForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

def is_user_authenticated(request):
    return request.user.is_authenticated

class LoginView(View):
    template = 'userauth/login.html'

    def get(self, request):
        if is_user_authenticated(request):
            return redirect(reverse('home:index'))
        form = LoginForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        if is_user_authenticated(request):
            return redirect(reverse('home:index'))
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(reverse('home:index'))
        
        return render(request, self.template, {'form': form, 'errors': form.errors})

class RegisterView(View):
    template = 'userauth/register.html'

    def get(self, request):
        if is_user_authenticated(request):
            return redirect(reverse('home:index'))
        form = UserCreationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        if is_user_authenticated(request):
            return redirect(reverse('home:index'))
        form = UserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.clean_password2
            user = authenticate(username=username, password=password)

            return render(request, 'userauth/success_register.html', {})

        return render(request, self.template, {'form': form, 'errors': form.errors})

def logout_user(request):
    logout(request)
    return redirect(reverse('userauth:login'))
