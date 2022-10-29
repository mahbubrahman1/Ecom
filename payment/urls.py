from django.urls import path

from .import views


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('pay/', views.payment, name='payment'),
    path('status/', views.complete_payment, name='complete_payment'),
    path('purchase/<val_id>/<tran_id>/', views.complete_purchase, name='complete_purchase'),
    path('orders/', views.view_order, name='orders'),
]
