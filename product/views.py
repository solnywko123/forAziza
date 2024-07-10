from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',)

    def create(self, request, *args, **kwargs):
        product_serializer = self.get_serializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product = product_serializer.save()
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def products_by_category(self, request, *args, **kwargs):
        category = request.query_params.get('category')
        queryset = self.queryset.filter(category=category)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


