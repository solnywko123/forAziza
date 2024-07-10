from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from account.serializers import User
from category.models import Category
from tests.factories import CategoryFactory


class CategoryAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.list_url = reverse('category-list')

    def test_create_category(self):
        data = {'name': 'New Category'}
        with self.assertNumQueries(6):
            response = self.client.post(self.list_url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Category.objects.count(), 1)
            self.assertEqual(Category.objects.last().name, 'New Category')

    def test_read_category(self):
        category = CategoryFactory(name='Test Category')
        detail_url = reverse('category-detail', args=[category.pk])
        with self.assertNumQueries(3):
            response = self.client.get(detail_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], 'Test Category')

    def test_update_category(self):
        category = CategoryFactory(name='Test Category')
        detail_url = reverse('category-detail', args=[category.pk])
        data = {'name': 'Updated Category'}
        with self.assertNumQueries(6):
            response = self.client.put(detail_url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            category.refresh_from_db()
            self.assertEqual(category.name, 'Updated Category')

    def test_delete_category(self):
        category = CategoryFactory(name='Test Category')
        detail_url = reverse('category-detail', args=[category.pk])
        with self.assertNumQueries(6):
            response = self.client.delete(detail_url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Category.objects.count(), 0)
