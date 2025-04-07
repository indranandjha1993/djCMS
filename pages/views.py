from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.http import Http404
from taggit.models import Tag

from .models import Page


class HomePageView(DetailView):
    """View for the homepage."""
    model = Page
    context_object_name = 'page'
    
    def get_object(self, queryset=None):
        """Get the homepage object."""
        try:
            return Page.objects.get(is_homepage=True, status=Page.STATUS_PUBLISHED)
        except Page.DoesNotExist:
            # If no homepage is set, get the first published page
            try:
                return Page.objects.filter(status=Page.STATUS_PUBLISHED).earliest('created_at')
            except Page.DoesNotExist:
                raise Http404("No published pages found")
    
    def get_template_names(self):
        """Return the template name to use."""
        page = self.get_object()
        return [page.template_name]


class PageDetailView(DetailView):
    """View for page detail."""
    model = Page
    context_object_name = 'page'
    
    def get_queryset(self):
        """Return only published pages."""
        return Page.objects.filter(status=Page.STATUS_PUBLISHED)
    
    def get_template_names(self):
        """Return the template name to use."""
        page = self.get_object()
        return [page.template_name]


class PageListView(ListView):
    """View for listing pages."""
    model = Page
    context_object_name = 'pages'
    template_name = 'pages/page_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        """Return only published pages."""
        return Page.objects.filter(status=Page.STATUS_PUBLISHED).order_by('-published_at')


class TagDetailView(ListView):
    """View for tag detail."""
    model = Page
    context_object_name = 'pages'
    template_name = 'pages/tag_detail.html'
    paginate_by = 10
    
    def get_queryset(self):
        """Return published pages with the given tag."""
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Page.objects.filter(
            status=Page.STATUS_PUBLISHED,
            tags__slug=self.tag.slug
        ).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context