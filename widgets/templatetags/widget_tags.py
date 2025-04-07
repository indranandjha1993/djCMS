from django import template
from django.template.loader import render_to_string
from django.db.models import Count

from widgets.models import WidgetArea, Widget
from blog.models import Post
from categories.models import Category
from taggit.models import Tag

register = template.Library()


@register.simple_tag(takes_context=True)
def render_widget_area(context, area_slug):
    """Render all widgets in a widget area."""
    try:
        area = WidgetArea.objects.get(slug=area_slug)
        widgets = area.widgets.filter(is_active=True).order_by('order')
        
        output = ""
        for widget in widgets:
            output += render_widget(context, widget)
        
        return output
    except WidgetArea.DoesNotExist:
        return ""


def render_widget(context, widget):
    """Render a single widget."""
    template = widget.get_template()
    
    # Prepare widget context based on type
    widget_context = {'widget': widget, 'title': widget.title}
    
    if widget.widget_type == Widget.WIDGET_RECENT_POSTS:
        count = widget.settings.get('count', 5)
        widget_context['posts'] = Post.objects.filter(
            status=Post.STATUS_PUBLISHED
        ).order_by('-published_at')[:count]
    
    elif widget.widget_type == Widget.WIDGET_POPULAR_POSTS:
        count = widget.settings.get('count', 5)
        widget_context['posts'] = Post.objects.filter(
            status=Post.STATUS_PUBLISHED
        ).order_by('-comment_count')[:count]
    
    elif widget.widget_type == Widget.WIDGET_CATEGORIES:
        count = widget.settings.get('count', 10)
        widget_context['categories'] = Category.objects.annotate(
            post_count=Count('blog_posts')
        ).filter(post_count__gt=0).order_by('-post_count')[:count]
    
    elif widget.widget_type == Widget.WIDGET_TAGS:
        count = widget.settings.get('count', 20)
        widget_context['tags'] = Tag.objects.annotate(
            post_count=Count('taggit_taggeditem_items')
        ).filter(post_count__gt=0).order_by('-post_count')[:count]
    
    # Add the request to the context
    if 'request' in context:
        widget_context['request'] = context['request']
    
    # Render the widget template
    return render_to_string(template, widget_context)


@register.inclusion_tag('widgets/widget_area.html', takes_context=True)
def show_widget_area(context, area_slug, template_name=None):
    """Show all widgets in a widget area."""
    try:
        area = WidgetArea.objects.get(slug=area_slug)
        widgets = area.widgets.filter(is_active=True).order_by('order')
        return {
            'area': area, 
            'widgets': widgets,
            'template_name': template_name,
            'request': context.get('request')
        }
    except WidgetArea.DoesNotExist:
        return {
            'area': None, 
            'widgets': [],
            'template_name': template_name,
            'request': context.get('request')
        }