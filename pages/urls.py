from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('pages/', views.PageListView.as_view(), name='page_list'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
]