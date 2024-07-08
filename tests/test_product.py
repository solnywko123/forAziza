from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from category.models import Category
from product.models import Product

class ProductCRUDTest(TestCase):

    def setUp(self):
        # Создаем тестовую категорию
        self.category = Category.objects.create(name='Тестовая категория')

    def test_create_product(self):
        product = Product.objects.create(
            title='Тестовый продукт',
            price=1000,
            description='Описание тестового продукта для проверки CRUD операций.',
            category=self.category,
            image=SimpleUploadedFile('test_image.jpg', content=b'', content_type='image/jpeg')
        )
        with self.assertNumQueries(1):
            self.assertEqual(Product.objects.count(), 1)
            self.assertEqual(product.title, 'Тестовый продукт')

    def test_read_product(self):
        product = Product.objects.create(
            title='Тестовый продукт',
            price=1000,
            description='Описание тестового продукта для проверки CRUD операций.',
            category=self.category,
            image=SimpleUploadedFile('test_image.jpg', content=b'', content_type='image/jpeg')
        )
        retrieved_product = Product.objects.get(title='Тестовый продукт')
        self.assertEqual(retrieved_product.description, 'Описание тестового продукта для проверки CRUD операций.')

    def test_update_product(self):
        product = Product.objects.create(
            title='Тестовый продукт',
            price=1000,
            description='Описание тестового продукта для проверки CRUD операций.',
            category=self.category,
            image=SimpleUploadedFile('test_image.jpg', content=b'', content_type='image/jpeg')
        )
        product.title = 'Обновленный продукт'
        product.save()
        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.title, 'Обновленный продукт')

    def test_delete_product(self):
        product = Product.objects.create(
            title='Тестовый продукт',
            price=1000,
            description='Описание тестового продукта для проверки CRUD операций.',
            category=self.category,
            image=SimpleUploadedFile('test_image.jpg', content=b'', content_type='image/jpeg')
        )
        product.delete()
        self.assertEqual(Product.objects.count(), 0)
