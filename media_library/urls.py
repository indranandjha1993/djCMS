from django.urls import path
from . import views

app_name = 'media_library'

urlpatterns = [
    path('', views.MediaLibraryListView.as_view(), name='media_list'),
    path('upload/', views.MediaUploadView.as_view(), name='media_upload'),
    path('<slug:slug>/', views.MediaItemDetailView.as_view(), name='media_detail'),
]