# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Visit, Country, Comment

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","first_name","last_name", "password"]

    def save(self):
     user = super().save()
     user.set_password(self.cleaned_data["password"])
     user.save()
     return user


class VisitForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset= Country.objects.all(),
        empty_label= "Select a country"
    )

    class Meta:
        model = Visit
        fields = ["city_name", "start_date", "end_date", "content", "photo", "country"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"] 
