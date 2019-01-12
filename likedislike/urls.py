from django.contrib.auth.decorators import login_required
from django.urls import path,re_path
from . import views
from blog.models import Post
from .models import LikeDislike
from books.models import Quote, Book, Author


app_name = 'ajax'

urlpatterns = [   
    re_path(r'^post/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Post, vote_type=LikeDislike.LIKE)),
        name='article_like'),
    re_path(r'^post/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Post, vote_type=LikeDislike.DISLIKE)),
        name='article_dislike'),
    re_path(r'^quote/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Quote, vote_type=LikeDislike.LIKE)),
        name='article_like'),
    re_path(r'^quote/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Quote, vote_type=LikeDislike.DISLIKE)),
        name='article_dislike'),
    re_path(r'^book/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Book, vote_type=LikeDislike.LIKE)),
        name='article_like'),
    re_path(r'^book/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Book, vote_type=LikeDislike.DISLIKE)),
        name='article_dislike'),
]