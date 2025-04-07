from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation

from core.models import PublishableModel, SEOModel
from core.user_models import User
from categories.models import Category
from comments.models import Comment


class Post(PublishableModel, SEOModel):
    """Model for blog posts."""
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    content = RichTextField(_("Content"))
    excerpt = models.TextField(_("Excerpt"), blank=True)
    featured_image = models.ImageField(_("Featured Image"), upload_to='blog/posts/', blank=True, null=True)
    
    # Relationships
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name=_("Author")
    )
    categories = models.ManyToManyField(
        Category,
        related_name='blog_posts',
        blank=True,
        verbose_name=_("Categories")
    )
    tags = TaggableManager(blank=True)
    comments = GenericRelation(Comment)
    
    # Additional fields
    is_featured = models.BooleanField(_("Featured"), default=False)
    allow_comments = models.BooleanField(_("Allow comments"), default=True)
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Get the absolute URL for the post."""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        """Override save method to generate slug."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def comment_count(self):
        """Get the number of approved comments."""
        return self.comments.filter(status=Comment.STATUS_APPROVED).count()
        
    # Add a method to get comments count for annotated querysets
    def get_comments_count(self):
        """Get the number of approved comments (for annotated querysets)."""
        if hasattr(self, 'comments_count'):
            return self.comments_count
        return self.comment_count
    
    @property
    def related_posts(self):
        """Get related posts based on categories and tags."""
        # Get posts with the same categories
        category_posts = Post.objects.filter(
            categories__in=self.categories.all(),
            status=self.STATUS_PUBLISHED
        ).exclude(pk=self.pk).distinct()
        
        # Get posts with the same tags
        tag_posts = Post.objects.filter(
            tags__name__in=self.tags.names(),
            status=self.STATUS_PUBLISHED
        ).exclude(pk=self.pk).distinct()
        
        # Combine and remove duplicates
        related = (category_posts | tag_posts).distinct()
        
        return related[:3]  # Return up to 3 related posts