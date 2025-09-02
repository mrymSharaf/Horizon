# forms.py
from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","first_name","last_name", "password"]

    def save(self):
     user = super().save()
     user.set_password(self.cleaned_data["password"])
     user.save()
     return user
