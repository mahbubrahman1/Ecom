from math import prod
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
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        context = {'carts': carts, 'order': order}
        return render(request, 'order/cart.html', context)

    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect('home')


# remove product from cart 
@login_required
def cart_remove(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.order_items.filter(item=product).exists():
            order_item = Cart.objects.filter(item=product, user=request.user, purchased=False)
            order_item = order_item[0]
            order.order_items.remove(order_item)
            order_item.delete()
            messages.info(request, 'Item removed from your cart.')
            return redirect('cart')

        else:
            messages.info(request, 'This product was not in your cart.')
            return redirect('home')

    else:
        messages.info(request, "Don't have an active order.")
        return redirect('home')

    
# increase item quantity
@login_required
def increase(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.order_items.filter(item=product).exists():
            order_item = Cart.objects.filter(item=product, user=request.user, purchased=False)
            order_item = order_item[0]

            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                return redirect('cart')

        else:
            messages.info(request, "This product is not in your cart")
            return redirect('home')
        
    else:
        messages.info(request, "You don't have an active order.")
        return redirect('home')


# decrease item quantity
@login_required
def decrease(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        
        if order.order_items.filter(item=product).exists():
            order_item = Cart.objects.filter(item=product, user=request.user, purchased=False)
            order_item = order_item[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                return redirect('cart')

            else:
                order.order_items.remove(order_item)
                order_item.delete()
                messages.warning(request, 'Product has been removed.')
                return redirect("cart")

        else:
            messages.info(request, "This product is not in your cart")
            return redirect('home')
            
    else:
        messages.info(request, "You don't have an active order.")
        return redirect('home')