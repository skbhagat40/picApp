from django import forms
from django.contrib.auth.models import User
from django.forms import widgets


class RegisterationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']
class LoginForm(forms.Form):
    username = forms.CharField(widget=widgets.TextInput)
    password = forms.CharField(widget=widgets.PasswordInput)