"""
URL Configuration for djCMS project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from pages.sitemaps import PageSitemap, CategorySitemap

sitemaps = {
    'pages': PageSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Include app URLs
    path('', include('pages.urls')),
    path('', include('core.urls')),
    path('categories/', include('categories.urls')),
    path('media-library/', include('media_library.urls')),
    path('comments/', include('comments.urls')),
    path('search/', include('search.urls')),
    path('blog/', include('blog.urls')),
    path('newsletter/', include('newsletter.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)