from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fk_name = 'menu'
    fields = ('title', 'item_type', 'page', 'category', 'url', 'target_blank', 'parent', 'order')
    raw_id_fields = ('page', 'category', 'parent')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'location', 'created_at')
    list_filter = ('location',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MenuItemInline]


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'item_type', 'parent', 'order')
    list_filter = ('menu', 'item_type')
    search_fields = ('title',)
    raw_id_fields = ('page', 'category', 'parent')
    
    fieldsets = (
        (None, {
            'fields': ('menu', 'title', 'order')
        }),
        (_('Link'), {
            'fields': ('item_type', 'page', 'category', 'url', 'target_blank')
        }),
        (_('Hierarchy'), {
            'fields': ('parent',)
        }),
    )


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)