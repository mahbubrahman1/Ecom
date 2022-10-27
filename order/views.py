from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from shop.models import Product
from .models import Cart, Order


# add item in cart
@login_required
def cart_add(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.order_items.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, 'This item quantity was updated.')
            return redirect('home')

        else:
            order.order_items.add(order_item[0])
            messages.info(request, 'Item added to your cart.')
            return redirect('home')
    
    else:
        order = Order(user=request.user)
        order.save()
        order.order_items.add(order_item[0])
        messages.info(request, 'Item add to your cart.')
        return redirect('home')


# view cart
def cart(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Cart.objects.filter(user=request.user, purchased=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        context = {'carts': carts, 'order': order}
        return render(request, 'order/cart.html', context)

    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect('home')