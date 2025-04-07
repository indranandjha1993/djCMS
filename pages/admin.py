from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Page, PageTemplate


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'template', 'parent', 'is_homepage', 'created_at', 'published_at', 'get_tags')
    list_filter = ('status', 'template', 'is_homepage', 'tags')
    search_fields = ('title', 'content', 'excerpt', 'tags__name')
    
    def get_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    get_tags.short_description = _("Tags")
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        (_('Publishing'), {
            'fields': ('status', 'published_at')
        }),
        (_('Organization'), {
            'fields': ('template', 'parent', 'categories', 'tags', 'order', 'is_homepage')
        }),
        (_('SEO'), {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 
                      'og_title', 'og_description', 'og_image')
        }),
    )
    
    filter_horizontal = ('categories',)
    
    actions = ['publish_pages', 'archive_pages', 'draft_pages']
    
    def publish_pages(self, request, queryset):
        for page in queryset:
            page.publish()
        self.message_user(request, _("Selected pages have been published."))
    publish_pages.short_description = _("Publish selected pages")
    
    def archive_pages(self, request, queryset):
        for page in queryset:
            page.archive()
        self.message_user(request, _("Selected pages have been archived."))
    archive_pages.short_description = _("Archive selected pages")
    
    def draft_pages(self, request, queryset):
        for page in queryset:
            page.draft()
        self.message_user(request, _("Selected pages have been set to draft."))
    draft_pages.short_description = _("Set selected pages to draft")


class PageTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'template', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


admin.site.register(Page, PageAdmin)
admin.site.register(PageTemplate, PageTemplateAdmin)