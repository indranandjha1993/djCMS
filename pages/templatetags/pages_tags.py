from django import template
from pages.models import Page

register = template.Library()


@register.simple_tag
def get_recent_pages(count=5):
    """Return the most recent published pages."""
    return Page.objects.filter(status=Page.STATUS_PUBLISHED).order_by('-published_at')[:count]


@register.simple_tag
def get_pages_by_template(template_slug, count=None):
    """Return pages with the specified template."""
    pages = Page.objects.filter(
        status=Page.STATUS_PUBLISHED,
        template__slug=template_slug
    ).order_by('-published_at')
    
    if count:
        return pages[:count]
    return pages


@register.inclusion_tag('pages/tags/page_list.html')
def show_page_list(pages, columns=3):
    """Render a list of pages."""
    return {
        'pages': pages,
        'columns': columns,
    }


@register.inclusion_tag('pages/tags/popular_tags.html')
def show_popular_tags(count=10):
    """Show the most popular tags."""
    from django.db.models import Count
    from taggit.models import Tag
    
    tags = Tag.objects.annotate(
        num_pages=Count('taggit_taggeditem_items')
    ).order_by('-num_pages')[:count]
    
    return {
        'tags': tags
    }