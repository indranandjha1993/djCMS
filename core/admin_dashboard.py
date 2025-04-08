from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.admin.models import LogEntry
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from blog.models import Post
from pages.models import Page
from comments.models import Comment
from core.user_models import User


@method_decorator(staff_member_required, name='dispatch')
class CustomAdminDashboard(TemplateView):
    """Custom admin dashboard view."""
    template_name = 'admin/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get counts for dashboard stats
        context['page_count'] = Page.objects.count()
        context['post_count'] = Post.objects.count()
        context['user_count'] = User.objects.count()
        context['comment_count'] = Comment.objects.count()
        
        # Get recent activity
        context['recent_actions'] = LogEntry.objects.select_related('content_type', 'user')[:10]
        
        # Add standard admin context
        from django.contrib import admin
        admin_context = admin.site.each_context(self.request)
        context.update(admin_context)
        
        # Add app_list for the standard admin modules section
        context['app_list'] = admin.site.get_app_list(self.request)
        context['show_changelinks'] = True
        
        return context