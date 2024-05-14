from django.urls import path

from . import views

app_name = 'ecommerce'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("item/<int:product_id>", views.item, name="item")
    ]