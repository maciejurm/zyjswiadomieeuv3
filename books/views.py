from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Genre, Book, Author, Quote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from taggit.models import Tag

def quotelist(request, tag_slug=None):
    quotes = Quote.objects.all()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        quotes = quotes.filter(tags__in=[tag])

    page = request.GET.get('page', 1)
    paginator = Paginator(quotes, 6)

    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        quotes = paginator.page(1)
    except EmptyPage:
        quotes = paginator.page(paginator.num_pages)
    return render(request, 'books/quotelist.html',
                {'quotes': quotes,
                'page': page,
                'tag': tag})

def quotedetail(request, slug):
    quote = get_object_or_404(Quote, slug=slug)
    books_count = Book.objects.filter(author=quote.book.author).count()
    return render(request, 'books/quotedetail.html',
                {'quote': quote,
                 'books_count': books_count})

def booklist(request):
    books = Book.objects.filter(active=True)
    return render(request, 'books/booklist.html',
                {'books': books})

def bookdetail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'books/bookdetail.html',
                {'book': book})

def authorlist(request):
    authors = Author.objects.all()
    return render(request, 'books/authorlist.html',
                {'authors': authors})

def authordetail(request, slug):
    author = get_object_or_404(Author, slug=slug)
    return render(request, 'books/author.html',
                {'author': author})
