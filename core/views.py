from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .user_models import User
from .forms import UserProfileForm, ContactForm


class UserProfileView(LoginRequiredMixin, DetailView):
    """View for user profile."""
    model = User
    template_name = 'core/user_profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self, queryset=None):
        """Get the user object."""
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user profile."""
    model = User
    form_class = UserProfileForm
    template_name = 'core/user_profile_update.html'
    success_url = reverse_lazy('core:profile')
    
    def get_object(self, queryset=None):
        """Get the user object."""
        return self.request.user
    
    def form_valid(self, form):
        """Handle valid form."""
        messages.success(self.request, _("Your profile has been updated."))
        return super().form_valid(form)


class ContactView(FormView):
    """View for contact form."""
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact_success')
    
    def form_valid(self, form):
        """Handle valid form."""
        form.send_email()
        return super().form_valid(form)


def contact_success(request):
    """View for contact form success."""
    return render(request, 'core/contact_success.html')