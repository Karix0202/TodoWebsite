from django.shortcuts import render
from django.views.generic import View
from .forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate

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
        form = UserCreationForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.clean_password2
            user = authenticate(username=username, password=password)

            return render(request, 'success_register.html', {})

        return render(request, self.template, {'form': form, 'errors': form.errors})