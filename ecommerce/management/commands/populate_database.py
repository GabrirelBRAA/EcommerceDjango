from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from ecommerce.models import Product, Category
from ecommerce.models import Image as Im
from django.core.files import File
import numpy as np
from tempfile import NamedTemporaryFile
from faker import Faker

from PIL import Image, ImageDraw

from random import random, randint

import stripe

class Command(BaseCommand):
    def hello(self):
        self.stdout.write("Hello World!")

    def create_image(self, name):
        pixel_data = np.random.randint(
            low=0,
            high=256,
            size=(1000, 1000, 3),
            dtype=np.uint8
        )
        image = Image.fromarray(pixel_data)
        draw = ImageDraw.Draw(image)
        draw.text((100, 400), name, fill=(0, 0, 0), font_size=100)
        image.save("./mock_images/" + name + ".jpg")
        return image


    categories = ["Computador", "Cadeira", "Sofá", "Casa", "Pedra", "Escola", "Cachorro", "Foo", "Bar", "Jogo"]

    def handle(self, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        fake = Faker("pt_BR")
        self.hello()
        self.stdout.write(str(args))
        self.stdout.write(str(kwargs))
        for category in self.categories:
            if (Category.objects.filter(name=category).first()) == None:
                new_category = Category(name=category)
                new_category.save()
            else:
                print(category + " already exists!")
        if Product.objects.filter(name="Cadeira1").first() == None:
            for category in self.categories:
                print(category)
                category_model = Category.objects.get(name=category)
                for i in range(1, 101):
                    product = Product(name=category + str(i),
                                      marca=fake.text(max_nb_chars=200),
                                      rating=(random() * 5.0),
                                      description=fake.text(max_nb_chars=1000),
                                      quantity= randint(0, 1000),
                                      price=(randint(0, 5000000)),
                                      category=category_model
                                      )
                    stripe_price = stripe.Price.create(currency="brl",
                                        unit_amount=product.price,
                                        product_data={"name": product.name})
                    product.stripe_price = stripe_price.id
                    product.save()






