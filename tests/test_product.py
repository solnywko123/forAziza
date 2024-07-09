from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from category.models import Category
from product.models import Product

User = get_user_model()

class ProductAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a category
        self.category = Category.objects.create(name='Test Category')

    # def test_create_product(self):
    #     url = reverse('product-list')
    #     data = {
    #         'title': 'New Product',
    #         'price': 100,
    #         'description': 'Product description',
    #         'category': self.category.name,  # Use category name for simplicity
    #         'image': ''  # Add image data if required
    #     }
    #     response = self.client.post(url, data, format='json')
    #     print(response.data)
    #     self.assertEqual(Product.objects.count(), 1)
    #     self.assertEqual(Product.objects.last().title, 'New Product')

    def test_read_product(self):
        product = Product.objects.create(title='Test Product', price=50, description='Product description', category=self.category)
        url = reverse('product-detail', args=[product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Product')
    #
    # def test_update_product(self):
    #     product = Product.objects.create(title='Test Product', price=50, description='Product description', category=self.category)
    #     url = reverse('product-detail', args=[product.pk])
    #     data = {'title': 'Updated Product'}
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     product.refresh_from_db()
    #     self.assertEqual(product.title, 'Updated Product')

    def test_delete_product(self):
        product = Product.objects.create(title='Test Product', price=50, description='Product description', category=self.category)
        url = reverse('product-detail', args=[product.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
