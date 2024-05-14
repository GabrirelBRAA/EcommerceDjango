from django.shortcuts import render, reverse
from django.http import HttpResponse

from .models import Product

# Create your views here.

app_name = '/ecommerce'

def index(request):

    products = Product.get_for_index()
    d = {'products': products}
    return render(request, "ecommerce/index.html", d)

def item(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "ecommerce/product.html", {"product": product, "app_name": app_name})

def login(request):
    if request.method == 'POST':
        pass
    return render(request, "ecommerce/login.html")

