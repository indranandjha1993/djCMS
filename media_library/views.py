from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from .models import MediaItem, MediaCategory


class MediaLibraryListView(LoginRequiredMixin, ListView):
    """View for listing media items."""
    model = MediaItem
    context_object_name = 'media_items'
    template_name = 'media_library/media_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = MediaItem.objects.all()
        
        # Filter by file type
        file_type = self.request.GET.get('type')
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                title__icontains=search_query
            ) | queryset.filter(
                description__icontains=search_query
            ) | queryset.filter(
                alt_text__icontains=search_query
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MediaCategory.objects.all()
        context['file_types'] = MediaItem.TYPE_CHOICES
        return context


class MediaItemDetailView(LoginRequiredMixin, DetailView):
    """View for media item detail."""
    model = MediaItem
    context_object_name = 'media_item'
    template_name = 'media_library/media_detail.html'


@method_decorator(csrf_exempt, name='dispatch')
class MediaUploadView(LoginRequiredMixin, View):
    """View for handling AJAX media uploads."""
    
    def post(self, request, *args, **kwargs):
        """Handle POST request."""
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        file = request.FILES['file']
        title = request.POST.get('title', file.name)
        
        # Create media item
        media_item = MediaItem.objects.create(
            title=title,
            file=file,
            uploaded_by=request.user
        )
        
        # Return JSON response
        return JsonResponse({
            'id': media_item.id,
            'title': media_item.title,
            'url': media_item.file.url,
            'file_type': media_item.file_type,
        })