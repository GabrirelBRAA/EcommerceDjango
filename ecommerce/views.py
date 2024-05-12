from django.shortcuts import render, reverse
from django.http import HttpResponse

from .models import Product

# Create your views here.

app_name = '/ecommerce'

def hello(request):

    products = Product.get_for_index()
    d = {'products': []}
    for query in products: #Maybe jut send the QuerySet to the template engine
        obj = {
            "name": query.name,
            "image": query.image,
            "id": query.id
        }
        d["products"].append(obj)

    d["app_name"] = app_name
    #print(reverse("hello"))
    return render(request, "ecommerce/index.html", d)

def item(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "ecommerce/product.html", {"product": product, "app_name": app_name})

def login(request):
    return render(request, "ecommerce/login.html")

