from django.urls import path

from . import views

app_name = 'ecommerce'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_user, name="login"),
    path("item/<int:product_id>", views.item, name="item"),
    path("logout", views.logoff, name='logout'),
    path('signin', views.signin, name='signin'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('shooping_cart', views.shopping_cart, name='shopping_cart')
    ]