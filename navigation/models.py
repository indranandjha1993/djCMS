from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from core.models import TimeStampedModel
from pages.models import Page
from categories.models import Category


class Menu(TimeStampedModel):
    """Model for menus."""
    LOCATION_HEADER = 'header'
    LOCATION_FOOTER = 'footer'
    LOCATION_SIDEBAR = 'sidebar'
    
    LOCATION_CHOICES = (
        (LOCATION_HEADER, _('Header')),
        (LOCATION_FOOTER, _('Footer')),
        (LOCATION_SIDEBAR, _('Sidebar')),
    )
    
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)
    location = models.CharField(_("Location"), max_length=20, choices=LOCATION_CHOICES, default=LOCATION_HEADER)
    
    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MenuItem(TimeStampedModel):
    """Model for menu items."""
    TYPE_PAGE = 'page'
    TYPE_CATEGORY = 'category'
    TYPE_CUSTOM = 'custom'
    
    TYPE_CHOICES = (
        (TYPE_PAGE, _('Page')),
        (TYPE_CATEGORY, _('Category')),
        (TYPE_CUSTOM, _('Custom URL')),
    )
    
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(_("Title"), max_length=100)
    item_type = models.CharField(_("Type"), max_length=20, choices=TYPE_CHOICES, default=TYPE_CUSTOM)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True, related_name='menu_items')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='menu_items')
    url = models.CharField(_("URL"), max_length=255, blank=True, help_text=_("Used only for custom URLs"))
    target_blank = models.BooleanField(_("Open in new tab"), default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")
        ordering = ['order']
    
    def __str__(self):
        return self.title
    
    @property
    def get_url(self):
        """Return the URL for this menu item."""
        if self.item_type == self.TYPE_PAGE and self.page:
            return self.page.get_absolute_url()
        elif self.item_type == self.TYPE_CATEGORY and self.category:
            return self.category.get_absolute_url()
        else:
            return self.url