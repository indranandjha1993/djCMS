from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Theme


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        (_('Colors'), {
            'fields': ('primary_color', 'secondary_color', 'accent_color')
        }),
        (_('Typography'), {
            'fields': ('font_family', 'heading_font_family')
        }),
        (_('Layout'), {
            'fields': ('container_width',)
        }),
        (_('Custom Code'), {
            'fields': ('custom_css', 'custom_js')
        }),
        (_('Branding'), {
            'fields': ('logo', 'favicon')
        }),
    )
    
    actions = ['activate_themes']
    
    def activate_themes(self, request, queryset):
        """Activate selected theme and deactivate others."""
        if queryset.count() > 1:
            self.message_user(request, _("Please select only one theme to activate."), level='error')
            return
        
        theme = queryset.first()
        theme.is_active = True
        theme.save()
        
        self.message_user(request, _(f"Theme '{theme.name}' has been activated."))
    activate_themes.short_description = _("Activate selected theme")


admin.site.register(Theme, ThemeAdmin)