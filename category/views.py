from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Category
from category.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
