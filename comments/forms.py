from django.forms import ModelForm
from .models import CommentPost
from django.contrib.auth.models import User

class CommentPostForm(ModelForm):
    class Meta:
        model = CommentPost
        fields = ['body']
