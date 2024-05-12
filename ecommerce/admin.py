from django.contrib import admin

from .models import Product, Sale, Order, Category, Image, PriceHistory

# Register your models here.

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(PriceHistory)
