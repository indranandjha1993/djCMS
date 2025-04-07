from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag

from .models import Post
from categories.models import Category
from core.user_models import User
from comments.models import Comment


class PostListView(ListView):
    """View for listing blog posts."""
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        """Return only published posts."""
        return Post.objects.filter(status=Post.STATUS_PUBLISHED).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(
            status=Post.STATUS_PUBLISHED,
            is_featured=True
        ).order_by('-published_at')[:3]
        
        # Get popular categories
        context['popular_categories'] = Category.objects.annotate(
            post_count=Count('blog_posts')
        ).filter(post_count__gt=0).order_by('-post_count')[:5]
        
        return context


class PostDetailView(DetailView):
    """View for blog post detail."""
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'
    
    def get_queryset(self):
        """Return only published posts."""
        return Post.objects.filter(status=Post.STATUS_PUBLISHED)
    
    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        
        # Get related posts
        context['related_posts'] = self.object.related_posts
        
        # Get popular posts
        context['popular_posts'] = Post.objects.filter(
            status=Post.STATUS_PUBLISHED
        ).annotate(
            comments_count=Count('comments', filter=Q(comments__status=Comment.STATUS_APPROVED))
        ).order_by('-comments_count')[:3]
        
        return context


class CategoryPostListView(ListView):
    """View for listing posts by category."""
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/category_post_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        """Return published posts for the given category."""
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status=Post.STATUS_PUBLISHED,
            categories=self.category
        ).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        """Add category to context."""
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostListView(ListView):
    """View for listing posts by tag."""
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/tag_post_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        """Return published posts for the given tag."""
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status=Post.STATUS_PUBLISHED,
            tags__slug=self.tag.slug
        ).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        """Add tag to context."""
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class AuthorPostListView(ListView):
    """View for listing posts by author."""
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/author_post_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        """Return published posts for the given author."""
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(
            status=Post.STATUS_PUBLISHED,
            author=self.author
        ).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        """Add author to context."""
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class AuthorDashboardView(LoginRequiredMixin, ListView):
    """View for author dashboard."""
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/author_dashboard.html'
    paginate_by = 10
    
    def get_queryset(self):
        """Return posts for the current user."""
        return Post.objects.filter(author=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        
        # Get post counts by status
        context['draft_count'] = Post.objects.filter(
            author=self.request.user,
            status=Post.STATUS_DRAFT
        ).count()
        
        context['published_count'] = Post.objects.filter(
            author=self.request.user,
            status=Post.STATUS_PUBLISHED
        ).count()
        
        context['archived_count'] = Post.objects.filter(
            author=self.request.user,
            status=Post.STATUS_ARCHIVED
        ).count()
        
        return context