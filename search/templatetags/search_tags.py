from django import template

register = template.Library()

@register.filter
def classname(obj):
    """Return the class name of an object."""
    return obj.__class__.__name__