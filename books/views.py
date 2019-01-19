from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Genre, Book, Author, Quote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from taggit.models import Tag
from dal import autocomplete
from .forms import BookForm, QuoteForm
from django.contrib import messages

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
    return render(request, 'books/quotedetail.html',
                {'quote': quote})

@login_required(login_url='/account/login/')
def quoteadd(request):
    if request.method == 'POST':
        quoteadd = QuoteForm(request.POST)
        if quoteadd.is_valid():
            form = quoteadd.save(commit=True)
            form.added_by = request.user
            form.save()
            quoteadd.save_m2m()
            messages.success(request, 'Cytat został dodany, ale czeka jeszcze na moderację. :)')
        else:
            messages.error(request, 'Błąd! Sprawdź czy wypełniłeś/aś poprawnie wszystkie pola.')
    else:
        quoteadd = QuoteForm()
    return render(request, 'books/quoteadd.html',
                  {'quoteadd': quoteadd})

def booklist(request):
    books = Book.objects.filter(active=True)
    return render(request, 'books/booklist.html',
                {'books': books})

def bookdetail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'books/bookdetail.html',
                {'book': book})

@login_required(login_url='/account/login/')
def bookadd(request):
    if request.method == 'POST':
        bookadd = BookForm(request.POST, request.FILES)
        if bookadd.is_valid():
            form = bookadd.save(commit=False)
            form.added_by = request.user
            form.save()
            bookadd.save_m2m()
            messages.success(request, 'Książka została dodana, ale czeka jeszcze na moderację. :)')
        else:
            messages.error(request, 'Błąd! Sprawdź czy wypełniłeś/aś poprawnie wszystkie pola.')
    else:
        bookadd = BookForm()
    return render(request, 'books/bookadd.html',
                  {'bookadd': bookadd})

class AuthorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Author.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

def authorlist(request):
    authors = Author.objects.all()
    return render(request, 'books/authorlist.html',
                {'authors': authors})

def authordetail(request, slug):
    author = get_object_or_404(Author, slug=slug)
    return render(request, 'books/author.html',
                {'author': author})


