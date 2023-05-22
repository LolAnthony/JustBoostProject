from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=30, help_text='Введите верный email адрес')

    class Meta:
        model = User
        fields = ['username', 'email']

