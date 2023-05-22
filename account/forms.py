from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']


class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
