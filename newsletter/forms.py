from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    """Form for newsletter subscription."""
    
    class Meta:
        model = Subscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': _('Your email address')}),
            'name': forms.TextInput(attrs={'placeholder': _('Your name (optional)')}),
        }
    
    def save(self, commit=True):
        """Generate confirmation token and save."""
        instance = super().save(commit=False)
        
        # Generate confirmation token if new subscriber
        if not instance.pk:
            instance.confirmation_token = get_random_string(64)
            instance.is_active = False
        
        if commit:
            instance.save()
        
        return instance