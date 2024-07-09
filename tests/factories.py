import factory
from django.utils.text import slugify
from factory import fuzzy
from category.models import Category
from product.models import Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Faker('sentence', nb_words=4)
    price = factory.Faker('random_int', min=10, max=100)
    description = factory.Faker('text')
    category = factory.SubFactory(CategoryFactory)
    image = factory.Faker("image_url")
