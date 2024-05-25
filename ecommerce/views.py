from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect

from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from random import randint
# Create your views here.

app_name = '/ecommerce'

def index(request):

    products = Product.get_for_index()
    d = {'products': products}
    return render(request, "ecommerce/index.html", d)

def item(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "ecommerce/product.html", {"product": product, "app_name": app_name})

def signin(request):
    if request.method == 'POST':
        print(request.POST['name'])
        print(request.POST['password'])
        if(request.POST['password'] == request.POST['confirmpassword']):
            user = User.objects.create_user(request.POST['name'], "email@gmail.com", request.POST['password'])
            login(request, user)
            return HttpResponseRedirect(reverse('ecommerce:index'))
        else:
            return render(request, "ecommerce/login.html", {'error': "password and confirmation password do not match"})
    return render(request, "ecommerce/login.html")

def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['name'], password=request.POST['password'])
        if(user != None):
            login(request, user)
            return HttpResponseRedirect(reverse('ecommerce:index'))
    return render(request, "ecommerce/login.html", {'error': "user or password incorrect"})


def logoff(request):
    if request.method == 'POST':
        print("Hello World 1")
        logout(request)
        print("Hello World 1")
    print("Hello World 2")
    return HttpResponseRedirect(reverse('ecommerce:index'))

def register(request):
    return render(request, "ecommerce/index.html")

def add_to_cart(request):
    if request.user.is_active and request.method == "POST":
        if "shopping_cart" not in request.session:
            request.session["shopping_cart"] = {}
            print("Huh")
        request.session["shopping_cart"].update({request.POST['id']: request.POST['quantity']})
        request.session.modified = True
        return HttpResponse(str(dict(request.session)))
    else:
        return HttpResponseRedirect(reverse('ecommerce:login'))

def shopping_cart(request):
    if "shopping_cart" in request.session:
        products = Product.objects.filter(id__in=request.session["shopping_cart"].keys())
        for product in products:
            product.quant = request.session["shopping_cart"].get(str(product.id))
        return render(request, 'ecommerce/shopping_cart.html', {"products": products})
    else:
        return render(request, 'ecommerce/shopping_cart.html', {"products": []})
