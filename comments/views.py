from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Comment
from .forms import CommentForm


@require_POST
def post_comment(request, content_type_id, object_id, parent_id=None):
    """Post a comment."""
    content_type = get_object_or_404(ContentType, pk=content_type_id)
    content_object = get_object_or_404(content_type.model_class(), pk=object_id)
    
    # Get parent comment if replying
    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, pk=parent_id)
    
    # Get IP and user agent
    ip_address = request.META.get('REMOTE_ADDR', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Create form with request data
    form = CommentForm(request.POST, content_object=content_object, 
                      user=request.user, parent=parent,
                      ip_address=ip_address, user_agent=user_agent)
    
    if form.is_valid():
        comment = form.save(commit=False)
        
        # Set content object
        comment.content_type = content_type
        comment.object_id = object_id
        
        # Set author if authenticated
        if request.user.is_authenticated:
            comment.author = request.user
        
        # Set parent if replying
        if parent:
            comment.parent = parent
        
        # Set IP and user agent
        comment.ip_address = ip_address
        comment.user_agent = user_agent
        
        # Auto-approve comments from authenticated users
        if request.user.is_authenticated:
            comment.status = Comment.STATUS_APPROVED
        
        comment.save()
        
        messages.success(request, _("Your comment has been posted."))
        if not request.user.is_authenticated:
            messages.info(request, _("Your comment will be visible after moderation."))
    else:
        messages.error(request, _("There was an error posting your comment."))
    
    # Redirect back to the content object
    return redirect(content_object.get_absolute_url())


@login_required
def delete_comment(request, comment_id):
    """Delete a comment."""
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Only allow the author or staff to delete
    if request.user == comment.author or request.user.is_staff:
        content_object = comment.content_object
        comment.delete()
        messages.success(request, _("Your comment has been deleted."))
        return redirect(content_object.get_absolute_url())
    else:
        messages.error(request, _("You don't have permission to delete this comment."))
        return redirect('/')


@login_required
def approve_comment(request, comment_id):
    """Approve a comment."""
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Only allow staff to approve
    if request.user.is_staff:
        comment.approve()
        messages.success(request, _("Comment has been approved."))
        return redirect(comment.content_object.get_absolute_url())
    else:
        messages.error(request, _("You don't have permission to approve comments."))
        return redirect('/')


@login_required
def reject_comment(request, comment_id):
    """Reject a comment."""
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Only allow staff to reject
    if request.user.is_staff:
        comment.reject()
        messages.success(request, _("Comment has been rejected."))
        return redirect(comment.content_object.get_absolute_url())
    else:
        messages.error(request, _("You don't have permission to reject comments."))
        return redirect('/')