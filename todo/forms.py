from django import forms
from .models import TodoGroup

class CreateTodoGroupForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    photo = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control'
        }
    ))
    class Meta:
        model = TodoGroup
        fields = ['name', 'photo', 'members']
