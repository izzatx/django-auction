from django import forms
from django.contrib.auth.models import User # This is the user library from django, not the user in the models.py
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']