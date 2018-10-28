from django import forms
from .models import TodoGroup, Todo
from friends.models import FriendRequest
from django.db.models import Q
from userauth.models import User

class CreateTodoGroupForm(forms.ModelForm):
    class Meta:
        model = TodoGroup
        fields = ['name', 'photo', 'members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'members': forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple form-input form-control'}),
        }
        

class AddTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['target', 'user', 'group', 'creator']
        widgets = {
            'target': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'user': forms.Select(attrs={
                'class': 'form-control'
            }),
        }