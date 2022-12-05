
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import RegistrationForm
from .models import Account
import json

# Create your views here.


class RegisterPageView(CreateView):
    template_name = 'registration/signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

