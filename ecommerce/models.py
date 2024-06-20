from django.db import models
from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator

#TODO better description for model classes (follow the google python class convention:
# https://stackoverflow.com/questions/13850049/what-is-the-proper-way-to-comment-code-in-python)


class Category(models.Model):
    """
    Category is a type of product. Ex: Computer, couches, refrigerators, etc...
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class PriceHistory(models.Model):
    """
    PriceHistory is used to store the old prices from Product instances.
    A new PriceHistory is generated every time a Product.price changes. See the overloaded Product.save to see
    how it happens.
    """
    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    price = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.product.name + " price at: " + str(self.date)

    class Meta:
        verbose_name_plural = "price histories"


class Product(models.Model):
    """
    Product represents a product that is sold on the site.
    It can have a variable number of images (see Image model), can be referenced by a Order model and is able to
    generate PriceHistory to archive its price changes.
    """

    name = models.CharField(max_length=200)
    marca = models.CharField(max_length=200, null=True, blank=True)
    rating = models.FloatField(default=0, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)])
    description = models.TextField(default="")
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(null=False, blank=False)
    stripe_price = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    # Here we store __original_price to see if it changes later
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_price = self.price

    def __str__(self):
        return self.name

    def decimal_price(self):
        return self.price * 1/100

    @staticmethod
    def get_for_index():
        return Product.objects.all().order_by('rating')[:5]

    def save(self, *args, **kwargs):
        """
        Product.save creates a PriceHistory if the price has changed from the original one.
        """
        if self.price != self.__original_price and self._state.adding is False:
            price_history = PriceHistory(product=self, price=self.__original_price)
            price_history.save()
        super(Product, self).save(*args, **kwargs)
        self.__original_price = self.price


class Image(models.Model):
    """
    Image references an Product and stores one image of the product. A product can have more than one image and thus
    be referenced by more than one Image model.
    Image.priority refers to the order the images will be shown to the user (from 0 as first to whatever number of
    images there are)
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    priority = models.IntegerField(default=0)  # needs a constraint here

    def get_url(self):
        return self.image.url

    def __str__(self):
        return self.image.url


class Sale(models.Model):
    """
    A Sale refers to a User and has a variable number of Orders, each referreing to a single Product.
    Prices should be consulted by consulting Sale.date with the matching PriceHistory or the current Product.price
    """

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

    def get_status(self):
        return self.STATUS_OPTIONS[self.status]


class StripeCheckout(models.Model):
    """
    This is used to store the checkout_session that stripe provides
    """
    stripe_id = models.CharField(max_length=255)
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)


class Order(models.Model):
    """
    Order is a part of a Sale, each order refers to a single product and the quantity of it on the Sale.
    Order.save alters Product.quantity, it subtracts Order.quantity to Product.quantity.
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_quantity = self.quantity

    # This needs to be atomic
    # This code is also very much weird and unreadable
    def save(self, *args, **kwargs):
        if self._state.adding is True:
            if(self.product.quantity - self.quantity) < 0:
                raise ValueError("Not enough products for order quantity")
            self.product.quantity = models.F("quantity") - self.quantity
            self.product.save(update_fields=["quantity"])
            self.__original_quantity = self.quantity
        elif self.__original_quantity != self.quantity:
            if (self.product.quantity - self.quantity + self.__original_quantity) < 0:
                raise ValueError("Not enough products for order quantity")
            self.product.quantity = models.F("quantity") + self.__original_quantity - self.quantity
            self.product.save(update_fields=["quantity"])
            self.__original_quantity = self.quantity
        super(Order, self).save(*args, **kwargs)


def generate_sale(user, shopping_cart):
    sale = Sale(user=user)
    sale.save()
    for product_id, quantity in shopping_cart.items():
        product = Product.objects.get(id=product_id)
        order = Order(sale=sale, product=product, quantity=int(quantity))
        order.save()
    return sale
