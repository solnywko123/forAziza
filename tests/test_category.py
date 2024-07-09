from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from account.serializers import User
from category.models import Category
from tests.factories import CategoryFactory


class CategoryAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.category = CategoryFactory(name='Test Category')  # Используем фабрику для создания категории

    def test_create_category(self):
        url = reverse('category-list')
        data = {'name': 'New Category'}
        response = self.client.post(url, data, format='json')
        with self.assertNumQueries(2):
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Category.objects.count(), 2)
            self.assertEqual(Category.objects.last().name, 'New Category')

    def test_read_category(self):
        url = reverse('category-detail', args=[self.category.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_update_category(self):
        url = reverse('category-detail', args=[self.category.pk])
        data = {'name': 'Updated Category'}
        response = self.client.put(url, data, format='json')
        with self.assertNumQueries(1):
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.category.refresh_from_db()
            self.assertEqual(self.category.name, 'Updated Category')

    def test_delete_category(self):
        url = reverse('category-detail', args=[self.category.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
