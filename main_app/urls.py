from django.urls import path
from . import views

urlpatterns = [
   path('auth/signup/', views.SignUpView.as_view(), name='sign-up'),
   
   path('visits/all/', views.VisitListView.as_view(), name='visit-list'),
   path('visits/<int:pk>/', views.VisitDetailView.as_view(), name='visit-details'),
   
]
