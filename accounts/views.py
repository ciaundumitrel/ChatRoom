
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from .forms import RegistrationForm, EditProfileForm
from .models import Account
import json

# Create your views here.


class RegisterPageView(CreateView):
    template_name = 'registration/signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')


class ProfilePageView(TemplateView):
    template_name = 'registration/profile.html'


class EditProfilePageView(UpdateView):
    template_name = 'registration/edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('home')
    model = Account

