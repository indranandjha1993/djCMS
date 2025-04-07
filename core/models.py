from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .user_models import User


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    created and modified fields.
    """
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        abstract = True


class PublishableModel(TimeStampedModel):
    """
    An abstract base class model that provides publishing functionality.
    """
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'
    
    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_PUBLISHED, _('Published')),
        (STATUS_ARCHIVED, _('Archived')),
    )
    
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )
    published_at = models.DateTimeField(_("Published at"), null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def publish(self):
        """Publish the content."""
        self.status = self.STATUS_PUBLISHED
        self.published_at = timezone.now()
        self.save()
    
    def archive(self):
        """Archive the content."""
        self.status = self.STATUS_ARCHIVED
        self.save()
    
    def draft(self):
        """Set content as draft."""
        self.status = self.STATUS_DRAFT
        self.save()


class SEOModel(models.Model):
    """
    An abstract base class model that provides SEO fields.
    """
    meta_title = models.CharField(_("Meta title"), max_length=100, blank=True)
    meta_description = models.TextField(_("Meta description"), blank=True)
    meta_keywords = models.CharField(_("Meta keywords"), max_length=255, blank=True)
    canonical_url = models.URLField(_("Canonical URL"), blank=True)
    og_title = models.CharField(_("Open Graph title"), max_length=100, blank=True)
    og_description = models.TextField(_("Open Graph description"), blank=True)
    og_image = models.ImageField(_("Open Graph image"), upload_to='og_images/', blank=True, null=True)
    
    class Meta:
        abstract = True