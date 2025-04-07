from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'is_featured', 'get_categories', 'get_tags', 'created_at', 'published_at')
    list_filter = ('status', 'is_featured', 'categories', 'tags', 'author')
    search_fields = ('title', 'content', 'excerpt', 'tags__name')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        (_('Publishing'), {
            'fields': ('status', 'published_at', 'author')
        }),
        (_('Organization'), {
            'fields': ('categories', 'tags', 'is_featured', 'allow_comments')
        }),
        (_('SEO'), {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 
                      'og_title', 'og_description', 'og_image')
        }),
    )
    
    filter_horizontal = ('categories',)
    
    actions = ['publish_posts', 'archive_posts', 'draft_posts', 'feature_posts', 'unfeature_posts']
    
    def get_categories(self, obj):
        return ", ".join(o.name for o in obj.categories.all())
    get_categories.short_description = _("Categories")
    
    def get_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    get_tags.short_description = _("Tags")
    
    def publish_posts(self, request, queryset):
        for post in queryset:
            post.publish()
        self.message_user(request, _("Selected posts have been published."))
    publish_posts.short_description = _("Publish selected posts")
    
    def archive_posts(self, request, queryset):
        for post in queryset:
            post.archive()
        self.message_user(request, _("Selected posts have been archived."))
    archive_posts.short_description = _("Archive selected posts")
    
    def draft_posts(self, request, queryset):
        for post in queryset:
            post.draft()
        self.message_user(request, _("Selected posts have been set as draft."))
    draft_posts.short_description = _("Set selected posts as draft")
    
    def feature_posts(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, _("Selected posts have been featured."))
    feature_posts.short_description = _("Feature selected posts")
    
    def unfeature_posts(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, _("Selected posts have been unfeatured."))
    unfeature_posts.short_description = _("Unfeature selected posts")


admin.site.register(Post, PostAdmin)