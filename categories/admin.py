from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'order', 'created_at')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    ordering = ('order', 'name')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'featured_image')
        }),
        (_('Organization'), {
            'fields': ('parent', 'order')
        }),
        (_('SEO'), {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 
                      'og_title', 'og_description', 'og_image')
        }),
    )


admin.site.register(Category, CategoryAdmin)