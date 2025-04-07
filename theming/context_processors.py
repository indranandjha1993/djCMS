from .models import Theme


def theme(request):
    """Context processor to add active theme to all templates."""
    active_theme = Theme.get_active_theme()
    
    return {
        'theme': active_theme,
    }