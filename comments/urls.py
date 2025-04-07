from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('post/<int:content_type_id>/<int:object_id>/', views.post_comment, name='post_comment'),
    path('post/<int:content_type_id>/<int:object_id>/<int:parent_id>/', views.post_comment, name='post_reply'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('approve/<int:comment_id>/', views.approve_comment, name='approve_comment'),
    path('reject/<int:comment_id>/', views.reject_comment, name='reject_comment'),
]