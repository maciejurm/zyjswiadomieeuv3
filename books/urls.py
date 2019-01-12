from django.urls import path, include
from . import views


app_name = 'books'

urlpatterns = [
    path('list/', views.booklist, name='books'),
    path('book/<slug>', views.bookdetail, name='book_detail'),
    path('quotes/', views.quotelist, name='quotes'),
    path('quotes/<slug>', views.quotedetail, name='quote'),
    path('quotes/tag/(<tag_slug>)/', views.quotelist, name='quotes_list_by_tag'),
    path('authors/', views.authorlist, name='authors'),
    path('authors/<slug>', views.authordetail, name='book_author'),
]
