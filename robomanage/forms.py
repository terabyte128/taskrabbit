__author__ = 'Sam'

from django import forms
from robomanage.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=64)
    password = forms.CharField(label="Password", max_length=64)
