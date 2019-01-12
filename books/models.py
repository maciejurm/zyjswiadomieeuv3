from django.db import models
from django.urls import reverse
from taggit_selectize.managers import TaggableManager
from django.contrib.auth.models import User
from stream_django.activity import Activity
from likedislike.models import LikeDislike
from django.contrib.contenttypes.fields import GenericRelation

class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model, Activity):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='book')
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey('author', on_delete=models.SET_NULL, null=True, related_name='author')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField()
    tags = TaggableManager()
    isbn = models.CharField(max_length=13)
    genre = models.ManyToManyField(Genre, help_text='Wybierz kategorie dla tej książki')
    active = models.BooleanField(default=False)
    votes = GenericRelation(LikeDislike, related_query_name='book')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('books:book_detail', args=[str(self.slug)])

    def __str__(self):
        return self.title

    @property
    def activity_actor_attr(self):
        return self.added_by

class Author(models.Model):
    photo = models.ImageField(upload_to='book-author')
    name = models.CharField(max_length=250)
    bio = models.TextField()
    date_birth = models.DateField(blank=True, null=True)
    date_death = models.DateField(blank=True, null=True)
    votes = GenericRelation(LikeDislike, related_query_name='author')
    slug = models.SlugField(max_length=250)

    def get_absolute_url(self):
        return reverse('books:book_author', args=[str(self.slug)])


    def get_books_count(self):
        return Book.objects.filter(author=self).count()

    def __str__(self):
        return self.name

class Quote(models.Model, Activity):
    quote = models.TextField()
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quote_author')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True, related_name='quote_book_author')
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    votes = GenericRelation(LikeDislike, related_query_name='quote')
    tags = TaggableManager()

    def __str__(self):
        return self.quote

    def get_absolute_url(self):
        return reverse('books:quote', args=[str(self.slug)])

    @property
    def activity_actor_attr(self):
        return self.added_by