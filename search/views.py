from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from django.conf import settings

from pages.models import Page
from categories.models import Category


class SearchView(ListView):
    """View for search results."""
    template_name = 'search/search_results.html'
    paginate_by = 10
    context_object_name = 'results'
    
    def get_queryset(self):
        """Return search results."""
        query = self.request.GET.get('q', '')
        
        if not query:
            return []
        
        # Store the query for use in the template
        self.query = query
        
        # Search in pages
        page_results = Page.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(excerpt__icontains=query) |
            Q(meta_title__icontains=query) |
            Q(meta_description__icontains=query) |
            Q(meta_keywords__icontains=query),
            status=Page.STATUS_PUBLISHED
        ).distinct()
        
        # Search in categories
        category_results = Category.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(meta_title__icontains=query) |
            Q(meta_description__icontains=query) |
            Q(meta_keywords__icontains=query)
        ).distinct()
        
        # Combine results
        results = list(page_results) + list(category_results)
        return results
    
    def get_context_data(self, **kwargs):
        """Add query to context."""
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context