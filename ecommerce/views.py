from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect

from .models import Product, Category, generate_sale, Sale, Order
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError

app_name = '/ecommerce'


'''
This page should probably show about 10 categories, if you want then to be set by an admin their names must not be hard coded 
'''
def index(request):
    categories = Category.objects.all()[:10]
    params = {}
    for category in categories:
        params[category] = Product.objects.filter(category=category)[:10]
    data = {"data" : params.items()}
    return render(request, "ecommerce/index.html", data)


'''
This page needs some front end treatment
'''
def item(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "ecommerce/product.html", {"product": product, "app_name": app_name})


'''
signup, this is actually a sign up and not a sign in
'''
def signin(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(username, "email@gmail.com", password)
            login(request, user)
            return HttpResponseRedirect(reverse('ecommerce:index'))
        else:
            login_form = LoginForm()
            return render(request, "ecommerce/login.html", {"login_form": login_form, "sign_form": form})
    login_form = LoginForm()
    signup_form = SignUpForm()
    return render(request, "ecommerce/login.html", {"login_form": login_form, "sign_form": signup_form})


'''
If its a POST this will try to login the user, if not it will return the login page
'''
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
                return HttpResponseRedirect(reverse('ecommerce:index'))
            else:
                signup_form = SignUpForm()
                form.add_error(None, ValidationError("username or password are incorrect"))
                return render(request, "ecommerce/login.html", {"login_form": form, "sign_form": signup_form})

    login_form = LoginForm()
    signup_form = SignUpForm()
    return render(request, "ecommerce/login.html", {"login_form": login_form, "sign_form": signup_form})


def logoff(request):
    if request.method == 'POST':
        logout(request)
    return HttpResponseRedirect(reverse('ecommerce:index'))


def add_to_cart(request):
    if request.user.is_active and request.method == "POST":
        if "shopping_cart" not in request.session:
            request.session["shopping_cart"] = {}
        request.session["shopping_cart"].update({request.POST['id']: request.POST['quantity']})
        request.session.modified = True
        return HttpResponseRedirect(reverse('ecommerce:index'))
    else:
        return HttpResponseRedirect(reverse('ecommerce:login'))


def shopping_cart(request):
    if "shopping_cart" in request.session:
        products = Product.objects.filter(id__in=request.session["shopping_cart"].keys())
        for product in products:
            product.quant = request.session["shopping_cart"].get(str(product.id)) #This is a hack
        return render(request, 'ecommerce/shopping_cart.html', {"products": products})
    else:
        return render(request, 'ecommerce/shopping_cart.html', {"products": []})


def aboutus(request):
    return render(request, 'ecommerce/aboutus.html') #Não está feito


'''
This view is not really checking if searchquery is populated or not, an error might occur here
'''
def search(request):
    search_query = request.GET['searchquery'] #Se não tiver uma search query?

    if request.GET.get('offset') != None:
        offset = int(request.GET['offset'])
        products = Product.objects.filter(name__contains=search_query)[offset:(offset + 10)]
        return render(request, 'ecommerce/search_update.html', {"products": products})

    products = Product.objects.filter(name__contains=search_query)[:20]
    return render(request, 'ecommerce/search.html', {"products": products, "searchquery": search_query})


def orders(request):
    sales = Sale.objects.prefetch_related('order_set').filter(user=request.user)

    for sale in sales:
        price = 0
        for order in sale.order_set.all():
            price += order.product.price
        sale.total = price

    return render(request, 'ecommerce/orders.html', {"sales": sales})


def create_sale(request):
    if request.method == "POST":
        user = request.user
        if "shopping_cart" in request.session:
            generate_sale(user, request.session['shopping_cart'])
            request.session['shopping_cart'] = {}
            request.session.modified = True
        return HttpResponse("Post Here!")
    else:
        return HttpResponseRedirect(reverse('ecommerce:index'))