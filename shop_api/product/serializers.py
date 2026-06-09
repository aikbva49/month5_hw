from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from . import models

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'products_count']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = models.Product
        fields = ['id', 'title', 'description', 'price', 'rating', 'reviews']

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=100)


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=3, max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    category_id = serializers.IntegerField(required=True)

    def validate_category_id(self, category_id):
        try:
            models.Category.objects.get(id=category_id)
        except models.Category.DoesNotExist:
            raise ValidationError('Категория с таким ID не существует!')
        return category_id

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=5)
    stars = serializers.IntegerField(required=False, default=1)
    product_id = serializers.IntegerField(required=True)

    def validate_product_id(self, product_id):
        try:
            models.Product.objects.get(id=product_id)
        except models.Product.DoesNotExist:
            raise ValidationError('Товар с таким ID не существует!')
        return product_id

    def validate_stars(self, stars):
        if stars < 1 or stars > 5:
            raise ValidationError('Оценка должна быть  от 1 до 5!')
        return stars