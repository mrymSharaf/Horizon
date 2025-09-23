from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import City, Visit, Comment, VisitLike, CommentLike, Country, Follow
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from main_app.forms import SignupForm, VisitForm , CommentForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'


class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    
    
class VisitListView(LoginRequiredMixin,ListView):
    model = Visit
    template_name = 'visit/visit-list.html'
    context_object_name = 'visits'
    
    def get_queryset(self):
        return Visit.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['liked_visits'] = set(VisitLike.objects.filter(user=user).values_list('visit_id', flat=True))
        return context


class VisitDetailView(LoginRequiredMixin,DetailView):
    model = Visit
    template_name = 'visit/visit-details.html'
    context_object_name = 'visit'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        comments = self.object.comments.all().order_by('-created_at')
        context['comments'] = comments
        context['liked_visits'] = set(VisitLike.objects.filter(user=user).values_list('visit_id', flat=True))


        if user.is_authenticated:
            context['did_like_visit'] = VisitLike.objects.filter(user=user, visit=self.object).exists()

            for comment in comments:
                comment.did_like = CommentLike.objects.filter(user=user, comment=comment).exists()
        else:
            context['did_like_visit'] = False

            for comment in comments:
                comment.did_like = False

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
            liked = False
        else:
            liked = True
    
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':     
            data = {
                'liked': liked,
                'count': visit.likes.count(),
                }
            return JsonResponse(data)
            
        return redirect('visit-details', pk=visit.pk) 
    


class ToggleVisitLikeFeed(LoginRequiredMixin, View):
    def post(self, request, pk):
        visit = Visit.objects.get(pk=pk)
        like, created = VisitLike.objects.get_or_create(user=request.user, visit=visit)
        if not created: 
            like.delete()
            liked = False
        else:
            liked = True
    
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':     
            data = {
                'liked': liked,
                'count': visit.likes.count(),
                }
            return JsonResponse(data)
            
        return redirect('visit-list') 
    

class ToggleCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if not created:  
            like.delete()
            liked = False
        else:
            liked = True
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {
            'liked': liked,
            'count': comment.likes.count(),
            }
            return JsonResponse(data)
            
        return redirect('visit-details', pk=comment.visit.pk)


class UserDetailView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'user/user-profile.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["visits"] = self.object.visits.all().order_by('-created_at')  
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user/user-update.html'
    form_class = UserUpdateForm

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse_lazy("user-details", kwargs={"pk": self.object.id})


class UserChangePassword(UserPassesTestMixin, PasswordChangeView):
    template_name = 'user/user-change-password.html'
    
    def test_func(self):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy("user-details", kwargs={"pk": self.request.user.pk})
    

class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'user/user-confirm-delete.html'
    success_url = reverse_lazy('sign-up')
    
    def test_func(self):
        return self.request.user == self.get_object()
    

class CountryDetailView(DetailView):
    model = Country
    template_name = 'country/country-details.html'
    context_object_name = 'country'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visits'] = self.get_object().visits.all().order_by('-created_at') 
        return context 
    

class Search(TemplateView):
    template_name = 'search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        query_request = self.request.GET.get('q', None)
        
        if query_request is None:
            query = ""
        else:
            query = query_request.strip()
            
        users = User.objects.none()
        countries = Country.objects.none()
        
        if query != "":
            user_filter = (
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
            users = User.objects.filter(user_filter)
            
            country_filter = Q(country_name__icontains=query)
            countries = Country.objects.filter(country_filter)
        
        context['query'] = query
        context['users'] = users
        context['countries'] = countries
        
        return context
    

def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('city_name')
    return render(request, 'city/city_dropdown_list_options.html', {'cities': cities})

class FollowersListView(ListView):
    model = Follow
    template_name = 'follow/followrs-list.html'
    context_object_name = 'followers'
    
    def get_queryset(self):
        return Follow.objects.filter(following_id= self.kwargs["pk"])


class FollowingListView(ListView):
    model = Follow
    template_name = 'follow/following-list.html'
    context_object_name = 'following'
    
    def get_queryset(self):
        return Follow.objects.filter(follower_id= self.kwargs["pk"])