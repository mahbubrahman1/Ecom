from django.shortcuts import render

from .models import Product


# homepage 
def home(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'shop/home.html', context)


# product details
def product_info(request, pk):
    product = Product.objects.get(id=pk)

    context = {'product': product}
    return render(request, 'shop/product-info.html', context)