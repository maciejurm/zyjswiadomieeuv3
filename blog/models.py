from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit_selectize.managers import TaggableManager
from stream_django.activity import Activity
from django.contrib.contenttypes.fields import GenericRelation
from likedislike.models import LikeDislike
from tinymce import HTMLField



class Post(models.Model, Activity):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog')
    body = HTMLField(verbose_name='Treść artykułu')
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    votes = GenericRelation(LikeDislike, related_query_name='post')
    slug = models.SlugField(max_length=255)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    @property
    def activity_actor_attr(self):
        return self.author