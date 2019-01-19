from django.urls import path, re_path
from . import views
from .views import AuthorAutocomplete

app_name = 'books'

urlpatterns = [
    path('list/', views.booklist, name='books'),
    path('book/<slug>', views.bookdetail, name='book_detail'),
    path('book/list/add/', views.bookadd, name='book_add'),
    path('quotes/', views.quotelist, name='quotes'),
    path('quotes/<slug>', views.quotedetail, name='quote'),
    path('quotes/quote/add/', views.quoteadd, name='quote_add'),
    path('quotes/tag/(<tag_slug>)/', views.quotelist, name='quotes_list_by_tag'),
    path('authors/', views.authorlist, name='authors'),
    path('authors/<slug>', views.authordetail, name='book_author'),
    re_path(
        r'^author-autocomplete/$',
        AuthorAutocomplete.as_view(),
        name='author-autocomplete',
    ),
]
