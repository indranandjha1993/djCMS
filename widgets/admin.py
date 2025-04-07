from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import WidgetArea, Widget


class WidgetInline(admin.TabularInline):
    model = Widget
    extra = 1
    fields = ('title', 'widget_type', 'order', 'is_active')


class WidgetAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'widget_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    inlines = [WidgetInline]
    
    def widget_count(self, obj):
        return obj.widgets.count()
    widget_count.short_description = _("Widgets")


class WidgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'widget_type', 'area', 'order', 'is_active')
    list_filter = ('widget_type', 'area', 'is_active')
    search_fields = ('title', 'content')
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'widget_type', 'area', 'order', 'is_active')
        }),
        (_('Content'), {
            'fields': ('content',),
            'classes': ('collapse',),
        }),
        (_('Settings'), {
            'fields': ('settings',),
            'classes': ('collapse',),
        }),
        (_('Custom Widget'), {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',),
        }),
    )


admin.site.register(WidgetArea, WidgetAreaAdmin)
admin.site.register(Widget, WidgetAdmin)