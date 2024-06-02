from django.core.management.base import BaseCommand, CommandError
from ecommerce.models import Product, Category
from ecommerce.models import Image as Im
from django.core.files import File
import numpy as np
from tempfile import NamedTemporaryFile
from faker import Faker

from PIL import Image, ImageDraw

from random import random, randint

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
                                      price=(random() * 50000),
                                      category=category_model
                                      )
                    product.save()



        '''
        macbook = Product.objects.get(name="Macbook")
        print("MacBook = " + macbook.name)
        computador = self.create_image("Computador")
        tf = NamedTemporaryFile()
        computador.save(tf, format="JPEG")
        image = Im(product=macbook, priority=1)
        image.image.save(name="computadormacbook.jpg",content=File(tf))
        print(image)
        print(getcwd())
        '''




