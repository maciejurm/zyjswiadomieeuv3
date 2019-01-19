from django.db import models
from django.urls import reverse
from taggit_selectize.managers import TaggableManager
from django.contrib.auth.models import User
from stream_django.activity import Activity
from likedislike.models import LikeDislike
from django.contrib.contenttypes.fields import GenericRelation
from tinymce import HTMLField
from django.utils.text import slugify

class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model, Activity):
    title = models.CharField(max_length=250, verbose_name='Tytuł')
    image = models.ImageField(upload_to='book', verbose_name='Grafika okładki')
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey('author', on_delete=models.SET_NULL, blank=True, null=True, related_name='author', verbose_name='Autor', help_text='Jeśli niema autora w bazie, dodaj jego imię i nazwisko w opisie, a moderacja doda książkę i edytuje pole.')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = HTMLField(verbose_name='Opis książki')
    tags = TaggableManager(blank=True, verbose_name='Tagi')
    isbn = models.CharField(max_length=13, blank=True, help_text='To pole może pozostać puste.')
    genre = models.ManyToManyField(Genre, help_text='Wybierz kategorie dla tej książki', blank=True, null=True)
    active = models.BooleanField(default=False)
    votes = GenericRelation(LikeDislike, related_query_name='book')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('books:book_detail', args=[str(self.slug)])

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Book.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

class Quote(models.Model, Activity):
    quote = models.TextField(verbose_name='Cytat')
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(Author, blank=True, null=True, on_delete=models.CASCADE, related_name='quote_author', verbose_name='Autor', help_text='Jeśli nie znajdziesz w bazie autora cytatu, po prostu dopisz go w polu "Cytat", a moderacja dodać autora i edytuje pole.')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True, related_name='quote_book_author', verbose_name='Książką', help_text='To pole może zostać puste, jeśli nie znasz książki z którego pochodzi cytat lub jeśli cytat to kogoś wypowiedź. Jeśli jednak niema książki w bazie, dopisz jej nazwę w polu cytat.')
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    votes = GenericRelation(LikeDislike, related_query_name='quote')
    tags = TaggableManager(blank=True, verbose_name='Tagi')

    def __str__(self):
        return self.quote

    def get_absolute_url(self):
        return reverse('books:quote', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        self.slug = slugify("{obj.quote}-{obj.id}".format(obj=self))
        super(Quote, self).save(*args, **kwargs)

    @property
    def activity_actor_attr(self):
        return self.added_by