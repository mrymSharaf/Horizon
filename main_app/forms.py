# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Visit, Country, Comment, Profile, City

class SignupForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ["username","first_name","last_name", "password"]

    def save(self, commit = False):
     user = super().save(commit)
     user.set_password(self.cleaned_data["password"])
     user.save()
     
     profile, created = Profile.objects.get_or_create(user=user)
     if self.cleaned_data.get("profile_photo"):
        profile.profile_photo= self.cleaned_data["profile_photo"]
        profile.save()

     return user


class VisitForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset= Country.objects.all(),
        empty_label= "Select a country"
    )
    
    city = forms.ModelChoiceField(
        queryset= City.objects.all(),
        empty_label= "Select a city"
    )

    class Meta:
        model = Visit
        fields = ["start_date", "end_date", "content", "photo", "country", "city"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class UserUpdateForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"] 
        
    def save(self, commit = True):
        user = super().save(commit)
        profile_photo = self.cleaned_data.get('profile_photo')
        profile, _ = Profile.objects.get_or_create(user=user)
        if profile_photo:
            profile.profile_photo = profile_photo
            profile.save()
        return user
