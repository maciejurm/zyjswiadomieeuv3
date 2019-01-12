from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from taggit.models import Tag
from .models import Post
from django.contrib.auth.models import User
from comments.models import CommentPost
from likedislike.models import LikeDislike
from comments.forms import CommentPostForm


def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 6)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                'blog/list.html',
                {'page': page,
                'posts': posts,
                'tag': tag})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-created_at')[:3]
    comments = post.postcomments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentPostForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentPostForm()
    return render(request,
                'blog/detail.html',
                {'post': post,
                'comments': comments,
                'comment_form': comment_form,
                'similar_posts': similar_posts})