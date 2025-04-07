from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings

from .user_models import User


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'avatar', 'website', 
                 'facebook', 'twitter', 'instagram', 'linkedin']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class ContactForm(forms.Form):
    """Contact form."""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': _('Your name')})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': _('Your email')})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': _('Subject')})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': _('Your message')})
    )
    
    def send_email(self):
        """Send email with form data."""
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        
        full_message = f"Name: {name}\nEmail: {email}\n\n{message}"
        
        recipients = [admin[1] for admin in settings.ADMINS]
        if not recipients:
            recipients = [settings.DEFAULT_FROM_EMAIL]
        
        send_mail(
            subject=f"Contact Form: {subject}",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        
        return True