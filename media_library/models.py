from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from core.models import TimeStampedModel

User = get_user_model()


class MediaCategory(TimeStampedModel):
    """Model for media categories."""
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)
    
    class Meta:
        verbose_name = _("Media Category")
        verbose_name_plural = _("Media Categories")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MediaItem(TimeStampedModel):
    """Model for media items."""
    TYPE_IMAGE = 'image'
    TYPE_DOCUMENT = 'document'
    TYPE_VIDEO = 'video'
    TYPE_AUDIO = 'audio'
    TYPE_OTHER = 'other'
    
    TYPE_CHOICES = (
        (TYPE_IMAGE, _('Image')),
        (TYPE_DOCUMENT, _('Document')),
        (TYPE_VIDEO, _('Video')),
        (TYPE_AUDIO, _('Audio')),
        (TYPE_OTHER, _('Other')),
    )
    
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    description = models.TextField(_("Description"), blank=True)
    alt_text = models.CharField(_("Alt Text"), max_length=255, blank=True)
    file = models.FileField(_("File"), upload_to='media_library/')
    file_type = models.CharField(_("File Type"), max_length=20, choices=TYPE_CHOICES, default=TYPE_OTHER)
    file_size = models.PositiveIntegerField(_("File Size"), help_text=_("Size in bytes"), default=0)
    width = models.PositiveIntegerField(_("Width"), null=True, blank=True, help_text=_("Width in pixels (for images)"))
    height = models.PositiveIntegerField(_("Height"), null=True, blank=True, help_text=_("Height in pixels (for images)"))
    categories = models.ManyToManyField(MediaCategory, blank=True, related_name='media_items')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_media')
    
    class Meta:
        verbose_name = _("Media Item")
        verbose_name_plural = _("Media Items")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set file type based on file extension
        if self.file:
            file_name = self.file.name.lower()
            if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')):
                self.file_type = self.TYPE_IMAGE
            elif file_name.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt')):
                self.file_type = self.TYPE_DOCUMENT
            elif file_name.endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm')):
                self.file_type = self.TYPE_VIDEO
            elif file_name.endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                self.file_type = self.TYPE_AUDIO
            else:
                self.file_type = self.TYPE_OTHER
                
            # Set file size
            if self.file.size:
                self.file_size = self.file.size
        
        super().save(*args, **kwargs)