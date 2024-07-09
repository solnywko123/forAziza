from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from category.models import Category
from category.serializers import CategorySerializer
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title',)
    filterset_fields = ('category',)

    def create(self, request, *args, **kwargs):
        category_name = request.data.get('category')

        # попытка найти категорию
        try:
            category_instance = Category.objects.get(name=category_name)
        except:
            category_serializer = CategorySerializer(data={'name': category_name})
            if category_serializer.is_valid():
                category_instance = category_serializer.save()
            else:
                return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # изменение запроса для добавления ID категории
        request.data['category'] = category_instance.id

        # сохранение продукта
        product_serializer = self.get_serializer(data=request.data)
        product_serializer.is_valid()
        product_serializer.save()
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)
