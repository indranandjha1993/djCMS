from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

from core.models import PublishableModel, SEOModel
from categories.models import Category


class PageTemplate(models.Model):
    """Model for page templates."""
    TEMPLATE_DEFAULT = 'default'
    TEMPLATE_FULL_WIDTH = 'full_width'
    TEMPLATE_SIDEBAR = 'sidebar'
    TEMPLATE_HOMEPAGE = 'homepage'
    
    TEMPLATE_CHOICES = (
        (TEMPLATE_DEFAULT, _('Default')),
        (TEMPLATE_FULL_WIDTH, _('Full Width')),
        (TEMPLATE_SIDEBAR, _('Sidebar')),
        (TEMPLATE_HOMEPAGE, _('Homepage')),
    )
    
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    template = models.CharField(
        _("Template"),
        max_length=50,
        choices=TEMPLATE_CHOICES,
        default=TEMPLATE_DEFAULT
    )
    description = models.TextField(_("Description"), blank=True)
    
    class Meta:
        verbose_name = _("Page Template")
        verbose_name_plural = _("Page Templates")
    
    def __str__(self):
        return self.name


class Page(PublishableModel, SEOModel):
    """Model for pages."""
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    content = RichTextField(_("Content"))
    excerpt = models.TextField(_("Excerpt"), blank=True)
    tags = TaggableManager(blank=True)
    featured_image = models.ImageField(_("Featured Image"), upload_to='pages/', blank=True, null=True)
    template = models.ForeignKey(
        PageTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pages'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='pages',
        verbose_name=_("Categories")
    )
    order = models.IntegerField(_("Order"), default=0)
    is_homepage = models.BooleanField(_("Is Homepage"), default=False)
    
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # If this page is set as homepage, unset any other homepage
        if self.is_homepage:
            Page.objects.filter(is_homepage=True).update(is_homepage=False)
            
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        if self.is_homepage:
            return reverse('pages:home')
        return reverse('pages:page_detail', kwargs={'slug': self.slug})
    
    @property
    def template_name(self):
        """Return the template file name."""
        if self.template:
            return f"pages/{self.template.template}.html"
        return "pages/default.html"