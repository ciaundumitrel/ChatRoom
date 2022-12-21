from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from accounts.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ['email', 'username']


class EditProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)
    username = forms.CharField(max_length=12, required=False)

    class Meta:
        model = Account
        fields = ['username', 'profile_image']

