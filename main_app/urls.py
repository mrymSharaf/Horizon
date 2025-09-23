from django.urls import path
from . import views

urlpatterns = [
   path('', views.HomeView.as_view(), name='home'),
   path('auth/signup/', views.SignUpView.as_view(), name='sign-up'),
   
   path('visits/all/', views.VisitListView.as_view(), name='visit-list'),
   path('visits/<int:pk>/', views.VisitDetailView.as_view(), name='visit-details'),
   path('visits/create/', views.VisitCreateView.as_view(), name='visit-create'),
   path('visits/<int:pk>/edit/', views.VisistUpdateView.as_view(), name='visit-update'),
   path('visits/<int:pk>/delete/', views.VisitDeleteView.as_view(), name='visit-delete'),
   
   path('comments/all/', views.CommentListView.as_view(), name='comment-list'),
   path('visits/<int:visit_id>/comments/add/', views.CommentCreateView.as_view(), name='comment-create'),
   path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
   
   path('visits/<int:pk>/like/', views.ToggleVisitLike.as_view(), name='toggle_visit_like'),
   path('visits/<int:pk>/like/feed/', views.ToggleVisitLikeFeed.as_view(), name='toggle_visit_like_feed'),
   path('comments/<int:pk>/like/', views.ToggleCommentLike.as_view(), name='toggle_comment_like'),
   
   path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-details'),
   path('users/<int:pk>/edit', views.UserUpdateView.as_view(), name='user-update'),
   path('user/changePassword/', views.UserChangePassword.as_view(), name='user-change-password'),
   path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
   path('users/<int:pk>/followers/', views.FollowersListView.as_view(), name='followers'),
   path('users/<int:pk>/following/', views.FollowingListView.as_view(), name='following'),
   
   path('country/<int:pk>/', views.CountryDetailView.as_view(), name='country-details'),
   
   path('search/', views.Search.as_view(), name='search'),
   
   path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]
