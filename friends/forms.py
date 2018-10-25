from django import forms

class AddFriendForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))