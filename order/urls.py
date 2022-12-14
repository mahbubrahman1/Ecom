from django.urls import path

from .import views


urlpatterns = [
    path('add/<str:pk>/', views.cart_add, name='add_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/<str:pk>/', views.cart_remove, name='remove'),
    path('increase/<str:pk>/', views.increase, name='increase'),
    path('decrease/<str:pk>/', views.decrease, name='decrease'),
]
