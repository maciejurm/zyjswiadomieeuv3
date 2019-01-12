from django import template

from ..models import Book

register = template.Library()

@register.simple_tag
def total_author_books():
    return Book.objects.filter(author=self).count()