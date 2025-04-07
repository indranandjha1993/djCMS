from django import template
from django.urls import reverse

from newsletter.forms import SubscriberForm

register = template.Library()


@register.inclusion_tag('newsletter/tags/subscribe_form.html')
def newsletter_subscribe_form():
    """Render newsletter subscription form."""
    form = SubscriberForm()
    action_url = reverse('newsletter:subscribe')
    return {
        'form': form,
        'action_url': action_url,
    }