from django.test import TestCase

from .models import Product, PriceHistory, Order, Sale
from django.contrib.auth.models import User

# Create your tests here.


def create_laptop_product():
    product = Product(
        name="Laptop",
        marca="Lenovo",
        rating=0.0,
        description="A very good computer",
        quantity=10,
        price=4000.0,
        category=None,
    )
    product.save()
    return product


class ProductModelTests(TestCase):

    def test_product_can_be_added(self):
        product = create_laptop_product()
        new_product = Product.objects.get(name="Laptop")
        self.assertEqual(product, new_product)

    def test_product_price_change_creates_price_history(self):
        product = create_laptop_product()
        product.price = 5000.0
        product.save()
        price_history = PriceHistory.objects.get(product=product)
        self.assertEqual(price_history.price, 4000.0)


class OrderModelTests(TestCase):
    """
    Each order should alter the corresponding Product.quantity until it reaches 0
    """
    def test_order_changes_product_quantity(self):
        product = create_laptop_product()
        user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='glass onion')
        user.save()
        sale = Sale(user=user)
        sale.save()
        order = Order(sale=sale, product=product, quantity=5)
        order.save()
        product.refresh_from_db()
        self.assertEqual(product.quantity, 5)
        order.quantity = 10
        order.save()
        product.refresh_from_db()
        self.assertEqual(product.quantity, 0)
        order.quantity = 0
        order.save()
        product.refresh_from_db()
        self.assertEqual(product.quantity, 10)

    """
    Order should not be able to make Product.quantity negative
    """
    def test_order_can_not_make_product_quantity_negative(self):
        product = create_laptop_product()
        user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='glass onion')
        user.save()
        sale = Sale(user=user)
        sale.save()
        order = Order(sale=sale, product=product, quantity=11)
        with self.assertRaises(ValueError):
            order.save()
        order2 = Order(sale=sale, product=product, quantity=99)
        with self.assertRaises(ValueError):
            order2.save()
