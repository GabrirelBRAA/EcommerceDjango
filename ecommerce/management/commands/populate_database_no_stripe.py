from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from ecommerce.models import Product, Category
from ecommerce.models import Image as Im
from django.core.files import File
from tempfile import NamedTemporaryFile
from faker import Faker

from PIL import Image, ImageDraw

from random import random, randint

class Command(BaseCommand):
    categories = ["Computador", "Cadeira", "Sofá", "Casa", "Pedra", "Escola", "Cachorro", "Foo", "Bar", "Jogo"]

    def handle(self, *args, **kwargs):
        fake = Faker("pt_BR")
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
                    product.save()


