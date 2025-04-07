from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

from comments.models import Comment
from comments.forms import CommentForm

register = template.Library()


@register.simple_tag
def get_comments_count(obj):
    """Return the number of approved comments for an object."""
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(
        content_type=content_type,
        object_id=obj.pk,
        status=Comment.STATUS_APPROVED
    ).count()


@register.simple_tag
def get_comments(obj):
    """Return all approved comments for an object."""
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(
        content_type=content_type,
        object_id=obj.pk,
        status=Comment.STATUS_APPROVED,
        parent=None  # Only top-level comments
    ).order_by('-created_at')


@register.inclusion_tag('comments/tags/comment_form.html')
def comment_form(obj, user=None):
    """Render a comment form for an object."""
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(content_object=obj, user=user)
    
    return {
        'form': form,
        'content_type_id': content_type.pk,
        'object_id': obj.pk,
        'user': user,
    }


@register.inclusion_tag('comments/tags/comment_list.html')
def comment_list(obj, user=None):
    """Render a list of comments for an object."""
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(
        content_type=content_type,
        object_id=obj.pk,
        status=Comment.STATUS_APPROVED,
        parent=None  # Only top-level comments
    ).order_by('-created_at')
    
    return {
        'comments': comments,
        'content_type_id': content_type.pk,
        'object_id': obj.pk,
        'user': user,
    }