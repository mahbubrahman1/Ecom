from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import BillingAddress
from .forms import BillingAddressForm
from order.models import Order


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