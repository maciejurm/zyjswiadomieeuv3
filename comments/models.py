from django.db import models
from django.contrib.auth.models import User
from blog.models import Post

class Comment(models.Model):
    body = models.TextField(verbose_name='Treść komentarza')
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)


    class Meta:
        abstract = True
        ordering = ('created_at',)

class CommentPost(Comment):
    post = models.ForeignKey(Post, related_name='postcomments', on_delete=models.CASCADE)