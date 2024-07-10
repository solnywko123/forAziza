from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from product.models import Product
from tests.factories import CategoryFactory, ProductFactory

User = get_user_model()


class ProductAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.list_url = reverse('product-list')

    def test_create_product(self):
        category = CategoryFactory(name='Test Category')
        product_data = ProductFactory.build()
        data = {
            'title': product_data.title,
            'price': product_data.price,
            'description': product_data.description,
            'category': category.id,
        }
        with self.assertNumQueries(9):
            response = self.client.post(self.list_url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Product.objects.count(), 1)
            self.assertEqual(Product.objects.last().title, product_data.title)

    def test_read_product(self):
        category = CategoryFactory(name='Test Category')
        product = ProductFactory(title='Test Product', price=50, description='Product description',
                                 category=category)
        detail_url = reverse('product-detail', args=[product.pk])
        with self.assertNumQueries(4):
            response = self.client.get(detail_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['title'], 'Test Product')

    def test_update_product(self):
        category = CategoryFactory(name='Test Category')
        product = ProductFactory(category=category)
        detail_url = reverse('product-detail', args=[product.pk])
        updated_title = 'Updated Product'
        data = {'title': updated_title}
        with self.assertNumQueries(6):
            response = self.client.patch(detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            product.refresh_from_db()
            self.assertEqual(product.title, updated_title)

    def test_delete_product(self):
        category = CategoryFactory(name='Test Category')
        product = ProductFactory(category=category)
        detail_url = reverse('product-detail', args=[product.pk])
        with self.assertNumQueries(5):
            response = self.client.delete(detail_url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Product.objects.count(), 0)
