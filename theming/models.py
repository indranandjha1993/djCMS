from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.cache import cache

from core.models import TimeStampedModel


class Theme(TimeStampedModel):
    """Model for themes."""
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)
    is_active = models.BooleanField(_("Is Active"), default=False)
    
    # Theme settings
    primary_color = models.CharField(_("Primary Color"), max_length=20, default="#3490dc")
    secondary_color = models.CharField(_("Secondary Color"), max_length=20, default="#ffed4a")
    accent_color = models.CharField(_("Accent Color"), max_length=20, default="#f66d9b")
    
    # Typography
    font_family = models.CharField(_("Font Family"), max_length=100, default="'Inter', sans-serif")
    heading_font_family = models.CharField(_("Heading Font Family"), max_length=100, blank=True)
    
    # Layout
    container_width = models.CharField(_("Container Width"), max_length=20, default="1200px")
    
    # Custom CSS/JS
    custom_css = models.TextField(_("Custom CSS"), blank=True)
    custom_js = models.TextField(_("Custom JavaScript"), blank=True)
    
    # Logo
    logo = models.ImageField(_("Logo"), upload_to='theme/logos/', blank=True, null=True)
    favicon = models.ImageField(_("Favicon"), upload_to='theme/favicons/', blank=True, null=True)
    
    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # If this theme is set as active, deactivate all other themes
        if self.is_active:
            Theme.objects.filter(is_active=True).update(is_active=False)
            
        super().save(*args, **kwargs)
        
        # Clear theme cache
        cache.delete('active_theme')
    
    @classmethod
    def get_active_theme(cls):
        """Get the active theme."""
        active_theme = cache.get('active_theme')
        if active_theme is None:
            try:
                active_theme = cls.objects.get(is_active=True)
                cache.set('active_theme', active_theme)
            except cls.DoesNotExist:
                # If no active theme, get the first one or create a default
                active_theme = cls.objects.first()
                if active_theme:
                    active_theme.is_active = True
                    active_theme.save()
                else:
                    active_theme = cls.objects.create(
                        name="Default Theme",
                        is_active=True
                    )
                cache.set('active_theme', active_theme)
        return active_theme