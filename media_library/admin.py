from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import MediaItem, MediaCategory


class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'file_size_display', 'thumbnail', 'uploaded_by', 'created_at')
    list_filter = ('file_type', 'categories', 'created_at')
    search_fields = ('title', 'description', 'alt_text')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    filter_horizontal = ('categories',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'alt_text', 'file')
        }),
        (_('Organization'), {
            'fields': ('categories',)
        }),
        (_('File Information'), {
            'fields': ('file_type', 'file_size', 'width', 'height', 'uploaded_by')
        }),
    )
    
    readonly_fields = ('file_type', 'file_size', 'width', 'height', 'uploaded_by')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set uploaded_by when creating a new object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
    
    def file_size_display(self, obj):
        """Display file size in human-readable format."""
        if obj.file_size < 1024:
            return f"{obj.file_size} bytes"
        elif obj.file_size < 1024 * 1024:
            return f"{obj.file_size / 1024:.1f} KB"
        else:
            return f"{obj.file_size / (1024 * 1024):.1f} MB"
    file_size_display.short_description = _("File Size")
    
    def thumbnail(self, obj):
        """Display thumbnail for image files."""
        if obj.file_type == MediaItem.TYPE_IMAGE:
            return format_html('<img src="{}" width="50" height="auto" />', obj.file.url)
        return "-"
    thumbnail.short_description = _("Thumbnail")


class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(MediaItem, MediaItemAdmin)
admin.site.register(MediaCategory, MediaCategoryAdmin)