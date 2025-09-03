from django.shortcuts import render, redirect
from django.views import View
from .models import Visit, Comment, VisitLike
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from main_app.forms import SignupForm, VisitForm , CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    
    
class VisitListView(LoginRequiredMixin,ListView):
    model = Visit
    template_name = 'visit/visit-list.html'
    context_object_name = 'visits'


class VisitDetailView(LoginRequiredMixin,DetailView):
    model = Visit
    template_name = 'visit/visit-details.html'
    context_object_name = 'visit'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
       
        user = self.request.user
        if user.is_authenticated:
            context['did_like_visit'] = VisitLike.objects.filter(user=user, visit=self.object).exists()
        else:
            context['did_like_visit'] = False

        return context


class VisitCreateView(LoginRequiredMixin, CreateView):
    model = Visit
    template_name = 'visit/visit-form.html'
    form_class = VisitForm
     
    def get_success_url(self):
        return reverse('visit-list')

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class VisistUpdateView(LoginRequiredMixin,UpdateView):
    model = Visit
    template_name = 'visit/visit-form.html'
    form_class = VisitForm
    context_object_name = 'visit'

    def get_success_url(self):
        return reverse('visit-list')


class VisitDeleteView(LoginRequiredMixin,DeleteView):
    model = Visit
    context_object_name = 'visit'
    
    def get_success_url(self):
        return reverse('visit-list')


class CommentListView(LoginRequiredMixin,ListView):
    model = Comment
    template_name = 'comment/comment-list.html'
    context_object_name = 'comments'


class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    template_name = 'comment/comment-form.html'
    form_class = CommentForm
     
    def get_success_url(self):
        return reverse('visit-details', kwargs={'pk': self.kwargs['visit_id']})

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.visit = Visit.objects.get(pk=self.kwargs.get('visit_id'))
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model = Comment
    context_object_name = "comment"
    
    def get_success_url(self):
        return reverse("visit-details", kwargs={"pk": self.object.visit.id})
    
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
    

class ToggleVisitLike(LoginRequiredMixin, View):
    def post(self, request, pk):
        visit = Visit.objects.get(pk=pk)
        like, created = VisitLike.objects.get_or_create(user=request.user, visit=visit)
        if not created: 
            like.delete()
        return redirect('visit-details', pk=visit.pk) 