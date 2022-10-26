from django.urls import path

from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<str:pk>/', views.product_info, name='product-info'),
]
