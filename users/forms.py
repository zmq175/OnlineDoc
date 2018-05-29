from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User, Profile


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('nickname', )
