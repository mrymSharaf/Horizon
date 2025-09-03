from django.shortcuts import render
from .models import Visit, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from main_app.forms import SignupForm, VisitForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    
    
class VisitListView(ListView):
    model = Visit
    template_name = 'visit/visit-list.html'
    context_object_name = 'visits'


class VisitDetailView(DetailView):
    model = Visit
    template_name = 'visit/visit-details.html'
    context_object_name = 'visit'


class VisitCreateView(LoginRequiredMixin, CreateView):
    model = Visit
    template_name = 'visit/visit-form.html'
    form_class = VisitForm
     
    def get_success_url(self):
        return reverse('visit-list')

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class VisistUpdateView(UpdateView):
    model = Visit
    template_name = 'visit/visit-form.html'
    form_class = VisitForm
    context_object_name = 'visit'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["start_date"] = Visit.start_date
        context["end_date"] = Visit.end_date
        return context
    
    
    def get_success_url(self):
        return reverse('visit-list')


class VisitDeleteView(DeleteView):
    model = Visit
    context_object_name = 'visit'
    
    def get_success_url(self):
        return reverse('visit-list')
