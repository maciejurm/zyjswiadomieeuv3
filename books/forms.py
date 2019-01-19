from django.forms import ModelForm
from .models import Book, Quote,Author
from dal import autocomplete
from . import urls


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'image', 'author', 'summary', 'tags', 'isbn' )
        widgets = {
            'author': autocomplete.ModelSelect2(url='books:author-autocomplete')
        }

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ('quote', 'author', 'book', 'tags')
        widgets = {
            'author': autocomplete.ModelSelect2(url='books:author-autocomplete')
        }