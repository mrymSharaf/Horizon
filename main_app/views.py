from django.shortcuts import render
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from main_app.forms import SignupForm

# Create your views here.

class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")