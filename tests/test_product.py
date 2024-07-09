from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from product.models import Product
from tests.factories import CategoryFactory, ProductFactory

User = get_user_model()


class ProductAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.category = CategoryFactory(name='Test Category')  # Используем фабрику для создания категории
        self.product = ProductFactory()

    def test_create_product(self):
        url = reverse('product-list')
        product_data = ProductFactory.build()
        data = {
            'title': product_data.title,
            'price': product_data.price,
            'description': product_data.description,
            'category': self.category.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.last().title, product_data.title)

    def test_read_product(self):
        product = ProductFactory(title='Test Product', price=50, description='Product description',
                                 category=self.category)  # Используем фабрику для создания продукта
        url = reverse('product-detail', args=[product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Product')

    def test_update_product(self):
        updated_title = 'Updated Product'
        data = {'title': updated_title}
        with self.assertNumQueries(5):
            res = self.client.patch(reverse("product-detail", kwargs={"pk": self.product.pk}), data=data)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            my_product = Product.objects.first()

            self.assertEqual(my_product.title, data["title"])

    def test_delete_product(self):
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
