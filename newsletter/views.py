from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import Subscriber
from .forms import SubscriberForm


class SubscribeView(CreateView):
    """View for newsletter subscription."""
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'newsletter/subscribe.html'
    success_url = reverse_lazy('newsletter:subscribe_success')
    
    def form_valid(self, form):
        """Send confirmation email."""
        response = super().form_valid(form)
        subscriber = self.object
        
        # Send confirmation email
        subject = _("Confirm your newsletter subscription")
        confirmation_url = self.request.build_absolute_uri(
            reverse_lazy('newsletter:confirm', kwargs={'token': subscriber.confirmation_token})
        )
        
        context = {
            'subscriber': subscriber,
            'confirmation_url': confirmation_url,
        }
        
        html_message = render_to_string('newsletter/emails/confirmation_email.html', context)
        plain_message = render_to_string('newsletter/emails/confirmation_email.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscriber.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return response


class SubscribeSuccessView(TemplateView):
    """View for successful subscription."""
    template_name = 'newsletter/subscribe_success.html'


def confirm_subscription(request, token):
    """Confirm newsletter subscription."""
    subscriber = get_object_or_404(Subscriber, confirmation_token=token)
    
    if not subscriber.confirmed_at:
        subscriber.confirm()
        messages.success(request, _("Your subscription has been confirmed. Thank you!"))
    else:
        messages.info(request, _("Your subscription was already confirmed."))
    
    return redirect('newsletter:confirm_success')


class ConfirmSuccessView(TemplateView):
    """View for successful confirmation."""
    template_name = 'newsletter/confirm_success.html'


def unsubscribe(request, token):
    """Unsubscribe from newsletter."""
    subscriber = get_object_or_404(Subscriber, confirmation_token=token)
    
    if request.method == 'POST':
        subscriber.is_active = False
        subscriber.save()
        messages.success(request, _("You have been unsubscribed from our newsletter."))
        return redirect('newsletter:unsubscribe_success')
    
    return render(request, 'newsletter/unsubscribe.html', {'subscriber': subscriber})


class UnsubscribeSuccessView(TemplateView):
    """View for successful unsubscription."""
    template_name = 'newsletter/unsubscribe_success.html'