import datetime

from django.db import models
from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator

'''
Category is a type of product. Ex: Computer, couches, refrigerators, etc...
'''
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


'''
PriceHistory is used to store the old prices from Product instances.
A new PriceHistory is generated every time a Product.price changes. See the overloaded Product.save to see
how it happens.
'''
class PriceHistory(models.Model):
    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    price = models.FloatField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.product.name + " price at: " + str(self.date)

    class Meta:
        verbose_name_plural = "price histories"


'''
Product represents a product that is sold on the site.
It can have a variable number of images (see Image model), can be referenced by a Order model and is able to generate
PriceHistory to archive its price changes.
'''
class Product(models.Model):

    name = models.CharField(max_length=200)
    marca = models.CharField(max_length=200, null=True, blank=True)
    rating = models.FloatField(default=0, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)])
    description = models.TextField(default="")
    quantity = models.IntegerField(default=0)
    price = models.FloatField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)


    #Here we store __original_price to see if it changes later
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_price = self.price

    def __str__(self):
        return self.name

    @staticmethod
    def get_for_index():
        return Product.objects.all().order_by('rating')[:5]


    '''
    Product.save creates a PriceHistory if the price has changed from the original one.
    '''
    def save(self, *args, **kwargs):
        if self.price != self.__original_price:
            price_history = PriceHistory(product=self, price=self.__original_price)
            price_history.save()
        super(Product, self).save(*args, **kwargs)
        self.__original_price = self.price


'''
Image references an Product and stores one image of the product. A product can have more than one image and thus
be referenced by more than one Image model.
Image.priority refers to the order the images will be shown to the user (from 0 as first to whatever number of images
there are)
'''
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    priority = models.IntegerField(default=0) #needs a constraint here

    def get_url(self):
        return self.image.url

    def __str__(self):
        return self.image.url


'''
A Sale refers to a User and has a variable number of Orders, each referreing to a single Product.
Prices should be consulted by consulting Sale.date with the matching PriceHistory or the current Product.price
'''
class Sale(models.Model):

    COMPLETE = "COMP"
    PAYMENT_PENDING = "PPND"
    DELIVERY_PENDING = "DPND"
    CANCELLED = "CANC"
    CANCELLED_WITH_PENDING_PAYMENT = "CPND"

    STATUS_OPTIONS = {
        COMPLETE: "Complete",
        PAYMENT_PENDING: "Payment Pending",
        DELIVERY_PENDING: "Delivery Pending",
        CANCELLED: "Cancelled",
        CANCELLED_WITH_PENDING_PAYMENT: "Cancelled With Pending Refund"
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=4, choices=STATUS_OPTIONS, default=PAYMENT_PENDING)

    def __str__(self):
        return "SID: " + str(self.id) + " " + self.STATUS_OPTIONS[self.status]


'''
Order is a part of a Sale, each order refers to a single product and the quantity of it on the Sale.
Order.save alters Product.quantity, it subtracts Order.quantity to Product.quantity.
'''
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_quantity = self.quantity


    #This needs to be atomic
    def save(self, *args, **kwargs):
        if(self._state.adding == True):
            if((self.product.quantity - self.quantity) < 0):
                raise ValueError("Not enough products for order quantity")
            self.product.quantity = models.F("quantity") - self.quantity
            self.product.save(update_fields=["quantity"])
            self.__original_quantity = self.quantity
        elif(self.__original_quantity != self.quantity):
            if((self.product.quantity - self.quantity + self.__original_quantity) < 0):
                raise ValueError("Not enough products for order quantity")
            self.product.quantity = models.F("quantity") + self.__original_quantity - self.quantity
            self.product.save(update_fields=["quantity"])
            self.__original_quantity = self.quantity
        super(Order, self).save(*args, **kwargs)

