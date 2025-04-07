from .models import Menu


def menus(request):
    """Context processor to add menus to all templates."""
    header_menu = Menu.objects.filter(location=Menu.LOCATION_HEADER).first()
    footer_menu = Menu.objects.filter(location=Menu.LOCATION_FOOTER).first()
    sidebar_menu = Menu.objects.filter(location=Menu.LOCATION_SIDEBAR).first()
    
    return {
        'header_menu': header_menu,
        'footer_menu': footer_menu,
        'sidebar_menu': sidebar_menu,
    }