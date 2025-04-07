from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from core.models import TimeStampedModel


class WidgetArea(TimeStampedModel):
    """Model for widget areas."""
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)
    
    class Meta:
        verbose_name = _("Widget Area")
        verbose_name_plural = _("Widget Areas")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Widget(TimeStampedModel):
    """Model for widgets."""
    WIDGET_TEXT = 'text'
    WIDGET_HTML = 'html'
    WIDGET_RECENT_POSTS = 'recent_posts'
    WIDGET_POPULAR_POSTS = 'popular_posts'
    WIDGET_CATEGORIES = 'categories'
    WIDGET_TAGS = 'tags'
    WIDGET_NEWSLETTER = 'newsletter'
    WIDGET_SOCIAL = 'social'
    WIDGET_IMAGE = 'image'
    WIDGET_HERO = 'hero'
    WIDGET_FEATURES = 'features'
    WIDGET_FEATURED_POSTS = 'featured_posts'
    WIDGET_CALL_TO_ACTION = 'call_to_action'
    WIDGET_CUSTOM = 'custom'
    
    WIDGET_TYPES = (
        (WIDGET_TEXT, _('Text')),
        (WIDGET_HTML, _('HTML')),
        (WIDGET_RECENT_POSTS, _('Recent Posts')),
        (WIDGET_POPULAR_POSTS, _('Popular Posts')),
        (WIDGET_CATEGORIES, _('Categories')),
        (WIDGET_TAGS, _('Tags')),
        (WIDGET_NEWSLETTER, _('Newsletter')),
        (WIDGET_SOCIAL, _('Social Links')),
        (WIDGET_IMAGE, _('Image')),
        (WIDGET_HERO, _('Hero')),
        (WIDGET_FEATURES, _('Features')),
        (WIDGET_FEATURED_POSTS, _('Featured Posts')),
        (WIDGET_CALL_TO_ACTION, _('Call to Action')),
        (WIDGET_CUSTOM, _('Custom')),
    )
    
    title = models.CharField(_("Title"), max_length=100)
    widget_type = models.CharField(_("Widget Type"), max_length=20, choices=WIDGET_TYPES)
    area = models.ForeignKey(
        WidgetArea,
        on_delete=models.CASCADE,
        related_name='widgets',
        verbose_name=_("Widget Area")
    )
    content = models.TextField(_("Content"), blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)
    
    # For custom widgets
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Content Type")
    )
    object_id = models.PositiveIntegerField(_("Object ID"), null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Widget settings
    settings = models.JSONField(_("Settings"), default=dict, blank=True)
    
    class Meta:
        verbose_name = _("Widget")
        verbose_name_plural = _("Widgets")
        ordering = ['area', 'order']
    
    def __str__(self):
        return f"{self.title} ({self.get_widget_type_display()})"
    
    def get_template(self):
        """Get the template for this widget type."""
        return f"widgets/types/{self.widget_type}.html"