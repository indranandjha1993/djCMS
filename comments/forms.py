from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for creating comments."""
    
    class Meta:
        model = Comment
        fields = ['content', 'author_name', 'author_email', 'author_url']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': _('Your comment')}),
            'author_name': forms.TextInput(attrs={'placeholder': _('Your name')}),
            'author_email': forms.EmailInput(attrs={'placeholder': _('Your email')}),
            'author_url': forms.URLInput(attrs={'placeholder': _('Your website')}),
        }
    
    def __init__(self, *args, **kwargs):
        self.content_object = kwargs.pop('content_object', None)
        self.user = kwargs.pop('user', None)
        self.parent = kwargs.pop('parent', None)
        self.ip_address = kwargs.pop('ip_address', None)
        self.user_agent = kwargs.pop('user_agent', None)
        
        super().__init__(*args, **kwargs)
        
        # If user is authenticated, hide name and email fields
        if self.user and self.user.is_authenticated:
            self.fields.pop('author_name')
            self.fields.pop('author_email')
    
    def save(self, commit=True):
        comment = super().save(commit=False)
        
        # Set content object
        if self.content_object:
            comment.content_type = ContentType.objects.get_for_model(self.content_object)
            comment.object_id = self.content_object.pk
        
        # Set author if user is authenticated
        if self.user and self.user.is_authenticated:
            comment.author = self.user
        
        # Set parent comment if replying
        if self.parent:
            comment.parent = self.parent
        
        # Set IP and user agent
        if self.ip_address:
            comment.ip_address = self.ip_address
        if self.user_agent:
            comment.user_agent = self.user_agent
        
        # Auto-approve comments from authenticated users
        if self.user and self.user.is_authenticated:
            comment.status = Comment.STATUS_APPROVED
        
        if commit:
            comment.save()
        
        return comment