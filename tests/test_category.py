from django.test import TestCase
from category.models import Category


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_create_category(self):
        category = Category.objects.create(name='New Category')
        with self.assertNumQueries(1):
            self.assertEqual(Category.objects.count(), 2)
            self.assertEqual(category.name, 'New Category')

    def test_read_category(self):
        category = Category.objects.get(name='Test Category')
        self.assertEqual(category.name, 'Test Category')

    def test_update_category(self):
        self.category.name = 'Updated Category'
        self.category.save()
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_delete_category(self):
        self.category.delete()
        self.assertEqual(Category.objects.count(), 0)
