from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.models import TimeStampedModel
from core.user_models import User


class Comment(TimeStampedModel):
    """Model for comments."""
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    
    STATUS_CHOICES = (
        (STATUS_PENDING, _('Pending')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_REJECTED, _('Rejected')),
    )
    
    # Generic relation to the commented object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Comment data
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True,
        verbose_name=_("Author")
    )
    author_name = models.CharField(_("Name"), max_length=100, blank=True)
    author_email = models.EmailField(_("Email"), blank=True)
    author_url = models.URLField(_("Website"), blank=True)
    
    content = models.TextField(_("Content"))
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    
    # Comment hierarchy
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name=_("Parent Comment")
    )
    
    # IP and user agent for spam detection
    ip_address = models.GenericIPAddressField(_("IP Address"), blank=True, null=True)
    user_agent = models.CharField(_("User Agent"), max_length=255, blank=True)
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']
    
    def __str__(self):
        if self.author:
            return f"Comment by {self.author.display_name}"
        return f"Comment by {self.author_name or 'Anonymous'}"
    
    @property
    def is_approved(self):
        """Check if the comment is approved."""
        return self.status == self.STATUS_APPROVED
    
    def approve(self):
        """Approve the comment."""
        self.status = self.STATUS_APPROVED
        self.save()
    
    def reject(self):
        """Reject the comment."""
        self.status = self.STATUS_REJECTED
        self.save()
    
    @property
    def get_author_name(self):
        """Get the author name."""
        if self.author:
            return self.author.display_name
        return self.author_name or _("Anonymous")