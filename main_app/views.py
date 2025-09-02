from django.shortcuts import render
from .models import Visit, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from main_app.forms import SignupForm

# Create your views here.

class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    
class VisitListView(ListView):
    model = Visit
    template_name = 'visit/visit-list.html'
    context_object_name = 'visits'