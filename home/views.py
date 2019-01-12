from django.shortcuts import render
from blog.models import Post
from books.models import Book, Quote, Author 
from events.models import Event

def home(request):
    posts = Post.objects.all()[:3]
    books = Book.objects.all()
    events = Event.objects.all()
    quotes = Quote.objects.all()
    authors = Author.objects.all()
    return render(request, 'home/home.html',
                {'posts': posts,
                'books': books,
                'events': events,
                'quotes': quotes,
                'authors': authors})