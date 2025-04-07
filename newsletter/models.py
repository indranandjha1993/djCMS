from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from core.models import TimeStampedModel


class Subscriber(TimeStampedModel):
    """Model for newsletter subscribers."""
    email = models.EmailField(_("Email"), unique=True)
    name = models.CharField(_("Name"), max_length=100, blank=True)
    is_active = models.BooleanField(_("Active"), default=True)
    confirmation_token = models.CharField(_("Confirmation token"), max_length=100, blank=True)
    confirmed_at = models.DateTimeField(_("Confirmed at"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def confirm(self):
        """Confirm the subscription."""
        self.is_active = True
        self.confirmed_at = timezone.now()
        self.confirmation_token = ''
        self.save()


class Newsletter(TimeStampedModel):
    """Model for newsletters."""
    STATUS_DRAFT = 'draft'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_SENT = 'sent'
    
    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_SCHEDULED, _('Scheduled')),
        (STATUS_SENT, _('Sent')),
    )
    
    title = models.CharField(_("Title"), max_length=200)
    subject = models.CharField(_("Subject"), max_length=200)
    content = models.TextField(_("Content"))
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )
    scheduled_at = models.DateTimeField(_("Scheduled at"), null=True, blank=True)
    sent_at = models.DateTimeField(_("Sent at"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletters")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def send(self):
        """Send the newsletter."""
        self.status = self.STATUS_SENT
        self.sent_at = timezone.now()
        self.save()
    
    def schedule(self, scheduled_time):
        """Schedule the newsletter."""
        self.status = self.STATUS_SCHEDULED
        self.scheduled_at = scheduled_time
        self.save()