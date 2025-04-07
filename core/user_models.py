from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Extended user model for djCMS."""
    bio = models.TextField(_("Biography"), blank=True)
    avatar = models.ImageField(_("Avatar"), upload_to='avatars/', blank=True, null=True)
    website = models.URLField(_("Website"), blank=True)
    
    # Social media fields
    facebook = models.URLField(_("Facebook"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    instagram = models.URLField(_("Instagram"), blank=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True)
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    @property
    def display_name(self):
        """Return the display name for the user."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username