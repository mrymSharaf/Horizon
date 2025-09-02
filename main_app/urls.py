from django.urls import path
from . import views

urlpatterns = [
   path('auth/signup/', views.SignUpView.as_view(), name='sign-up'),
   
]
