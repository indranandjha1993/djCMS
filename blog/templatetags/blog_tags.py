from django import template
from django.db.models import Count, Q

from blog.models import Post
from categories.models import Category
from comments.models import Comment

register = template.Library()


@register.simple_tag
def get_recent_posts(count=5):
    """Return recent published posts."""
    return Post.objects.filter(
        status=Post.STATUS_PUBLISHED
    ).order_by('-published_at')[:count]


@register.simple_tag
def get_featured_posts(count=3):
    """Return featured published posts."""
    return Post.objects.filter(
        status=Post.STATUS_PUBLISHED,
        is_featured=True
    ).order_by('-published_at')[:count]


@register.simple_tag
def get_popular_posts(count=5):
    """Return popular published posts based on comment count."""
    return Post.objects.filter(
        status=Post.STATUS_PUBLISHED
    ).annotate(
        comments_count=Count('comments', filter=Q(comments__status=Comment.STATUS_APPROVED))
    ).order_by('-comments_count')[:count]


@register.simple_tag
def get_popular_categories(count=5):
    """Return popular categories based on post count."""
    return Category.objects.annotate(
        post_count=Count('blog_posts')
    ).filter(post_count__gt=0).order_by('-post_count')[:count]


@register.inclusion_tag('blog/tags/recent_posts.html')
def show_recent_posts(count=5):
    """Render recent posts."""
    posts = get_recent_posts(count)
    return {'posts': posts}


@register.inclusion_tag('blog/tags/featured_posts.html')
def show_featured_posts(count=3):
    """Render featured posts."""
    posts = get_featured_posts(count)
    return {'posts': posts}


@register.inclusion_tag('blog/tags/popular_posts.html')
def show_popular_posts(count=5):
    """Render popular posts."""
    posts = get_popular_posts(count)
    return {'posts': posts}