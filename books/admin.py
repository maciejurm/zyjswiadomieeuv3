from django.contrib import admin
from .models import Genre, Book, Author, Quote

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Quote)