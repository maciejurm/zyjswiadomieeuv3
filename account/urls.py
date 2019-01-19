from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('user/<username>', views.user_detail, name='user_detail'),
    path('follow/', views.FollowView.as_view(), name='follow'),
    re_path(r'^unfollow/(?P<target_id>\d+)/', views.UnfollowView.as_view(),
    name='unfollow'),
    path('timeline/', views.timeline, name='timeline_feed'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),
    path('register/', views.signup, name='register'),
    path('edit/', views.edit, name='edit'),
    path('polityka-prywatnosci/', views.privacy_policy, name='polityka'),
    re_path(r'^settings/$', views.settings, name='settings'),
    re_path(r'^settings/password/$', views.password, name='password'),
]
