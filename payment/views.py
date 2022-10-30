from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sslcommerz_python.payment import SSLCSession
from django.urls import reverse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

from .models import BillingAddress
from .forms import BillingAddressForm
from order.models import Order, Cart


# checkout 
@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingAddressForm(instance=saved_address)

    if request.method == 'POST':
        form = BillingAddressForm(request.POST, instance=saved_address)

        if form.is_valid():
            form.save()
            form = BillingAddressForm(instance=saved_address)
            messages.success(request, 'Shipping address saved.')

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_total = order_qs[0].get_totals()

    context = {'form': form, 'order_items': order_items, 'order_total': order_total, 'saved_address': saved_address}
    return render(request, 'payment/checkout.html', context) 


# pay 
@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    
    if not saved_address.is_fully_filled():
        messages.info(request, 'Please complete shipping address!')
        return redirect('checkout')

    if not request.user.profile.is_fully_filled():
        messages.info(request, 'Please complete profile details!')
        return redirect('profile')

    store_id = 'abc635cd1a071119'
    API_key = 'abc635cd1a071119@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass= API_key)

    status_url = request.build_absolute_uri(reverse('complete_payment'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_items_count = order_qs[0].order_items.count()
    order_total = order_qs[0].get_totals()

    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=order_items_count, shipping_method='Courier', product_profile='None')

    user = request.user
    mypayment.set_customer_info(name=user.profile.full_name, email=user.email, address1=user.profile.address_one, address2=user.profile.address_one, city=user.profile.city, postcode=user.profile.zipcode, country=saved_address.country, phone=user.profile.phone)

    mypayment.set_shipping_info(shipping_to=user.profile.full_name, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)

    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])


# complete payment 
@csrf_exempt
def complete_payment(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']

        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request, 'Your payment completed successfully')
            return HttpResponseRedirect(reverse('complete_purchase', kwargs={'val_id': val_id, 'tran_id': tran_id}))
        
        elif status == 'FAILED':
            messages.warning(request, 'Your payment failed! Please try again.')


    return render(request, 'payment/complete-payment.html')


# empty cart section
@login_required
def complete_purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    order_id = tran_id
    order.ordered = True
    order.order_id = order_id
    order.payment_id = val_id
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()

    return HttpResponseRedirect(reverse('home'))


# view customer orders
@login_required
def view_order(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {'orders': orders}
    
    except:
        messages.warning(request, 'You do not have an active order')

    return render(request, 'payment/order.html', context)
