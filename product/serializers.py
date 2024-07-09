from rest_framework import serializers
from category.models import Category
from category.serializers import CategorySerializer
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        category_name = validated_data.pop('category')
        category, created = Category.objects.get_or_create(name=category_name)
        product = Product.objects.create(category=category, **validated_data)
        return product
