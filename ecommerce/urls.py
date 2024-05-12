from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'ecommerce'
urlpatterns = [
    path("", views.hello, name="hello"),
    path("login", views.login, name="login"),
    path("item/<int:product_id>", views.item, name="item")
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)