from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_author_name', 'content_type', 'object_id', 'status', 'created_at')
    list_filter = ('status', 'content_type', 'created_at')
    search_fields = ('author_name', 'author_email', 'content')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('content_type', 'object_id', 'content')
        }),
        (_('Author'), {
            'fields': ('author', 'author_name', 'author_email', 'author_url')
        }),
        (_('Status'), {
            'fields': ('status',)
        }),
        (_('Hierarchy'), {
            'fields': ('parent',)
        }),
        (_('Meta'), {
            'fields': ('ip_address', 'user_agent')
        }),
    )
    
    readonly_fields = ('content_type', 'object_id', 'ip_address', 'user_agent')
    raw_id_fields = ('author', 'parent')
    
    actions = ['approve_comments', 'reject_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(status=Comment.STATUS_APPROVED)
        self.message_user(request, _("Selected comments have been approved."))
    approve_comments.short_description = _("Approve selected comments")
    
    def reject_comments(self, request, queryset):
        queryset.update(status=Comment.STATUS_REJECTED)
        self.message_user(request, _("Selected comments have been rejected."))
    reject_comments.short_description = _("Reject selected comments")


admin.site.register(Comment, CommentAdmin)