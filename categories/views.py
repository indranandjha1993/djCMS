from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Category
from pages.models import Page


class CategoryListView(ListView):
    """View for listing categories."""
    model = Category
    context_object_name = 'categories'
    template_name = 'categories/category_list.html'
    
    def get_queryset(self):
        """Return only top-level categories."""
        return Category.objects.filter(parent=None).order_by('order', 'name')


class CategoryDetailView(DetailView):
    """View for category detail."""
    model = Category
    context_object_name = 'category'
    template_name = 'categories/category_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get pages associated with this category
        category = self.get_object()
        context['pages'] = Page.objects.filter(
            status=Page.STATUS_PUBLISHED,
            categories=category
        ).order_by('-published_at')
        
        # Get subcategories
        context['subcategories'] = Category.objects.filter(parent=category).order_by('order', 'name')
        
        return context