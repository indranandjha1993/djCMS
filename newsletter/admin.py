from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Subscriber, Newsletter


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'confirmed_at', 'created_at')
    list_filter = ('is_active', 'created_at', 'confirmed_at')
    search_fields = ('email', 'name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected subscribers have been activated."))
    activate_subscribers.short_description = _("Activate selected subscribers")
    
    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected subscribers have been deactivated."))
    deactivate_subscribers.short_description = _("Deactivate selected subscribers")


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'status', 'scheduled_at', 'sent_at', 'created_at')
    list_filter = ('status', 'created_at', 'sent_at')
    search_fields = ('title', 'subject', 'content')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'subject', 'content')
        }),
        (_('Status'), {
            'fields': ('status', 'scheduled_at', 'sent_at')
        }),
    )
    
    readonly_fields = ('sent_at',)
    
    actions = ['send_newsletters', 'schedule_newsletters']
    
    def send_newsletters(self, request, queryset):
        for newsletter in queryset:
            newsletter.send()
        self.message_user(request, _("Selected newsletters have been sent."))
    send_newsletters.short_description = _("Send selected newsletters")
    
    def schedule_newsletters(self, request, queryset):
        scheduled_time = timezone.now() + timezone.timedelta(hours=1)
        for newsletter in queryset:
            newsletter.schedule(scheduled_time)
        self.message_user(request, _("Selected newsletters have been scheduled."))
    schedule_newsletters.short_description = _("Schedule selected newsletters for 1 hour from now")


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Newsletter, NewsletterAdmin)