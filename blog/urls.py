from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from .models import Post
from likedislike.models import LikeDislike
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug>', views.post_detail, name='post_detail'),
    path('tag/(<tag_slug>)/', views.post_list, name='post_list_by_tag'),
]
