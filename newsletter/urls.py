from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('subscribe/success/', views.SubscribeSuccessView.as_view(), name='subscribe_success'),
    path('confirm/<str:token>/', views.confirm_subscription, name='confirm'),
    path('confirm/success/', views.ConfirmSuccessView.as_view(), name='confirm_success'),
    path('unsubscribe/<str:token>/', views.unsubscribe, name='unsubscribe'),
    path('unsubscribe/success/', views.UnsubscribeSuccessView.as_view(), name='unsubscribe_success'),
]