from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from . import serializers
from . import models 

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = models.Category.objects.annotate(products_count=Count('products'))
        data = serializers.CategorySerializer(categories, many=True).data
        return Response(data=data)
        
    elif request.method == 'POST':
        serializer = serializers.CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        name = serializer.validated_data.get('name')
        
        category = models.Category.objects.create(name=name)
        
        return Response(
            data=serializers.CategorySerializer(category).data, 
            status=status.HTTP_201_CREATED
        )

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = models.Category.objects.annotate(products_count=Count('products')).get(id=id)
    except models.Category.DoesNotExist:
        return Response(data={'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        data = serializers.CategorySerializer(category).data
        return Response(data=data)
        
    elif request.method == 'PUT':
        serializer = serializers.CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get('name')
        category.save()
        
        return Response(
            data=serializers.CategorySerializer(category).data, 
            status=status.HTTP_200_OK
        )
        
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = models.Product.objects.select_related('category').all()
        data = serializers.ProductSerializer(products, many=True).data
        return Response(data=data)
        
    elif request.method == 'POST':
        serializer = serializers.ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')
        
        product = models.Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )
        return Response(
            data=serializers.ProductSerializer(product).data, 
            status=status.HTTP_201_CREATED
        )


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = models.Product.objects.get(id=id)
    except models.Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        data = serializers.ProductSerializer(product).data
        return Response(data=data)
        
    elif request.method == 'PUT':
        serializer = serializers.ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        product.save()
        
        return Response(
            data=serializers.ProductSerializer(product).data, 
            status=status.HTTP_200_OK
        )
        
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = models.Review.objects.select_related('product').all()
        data = serializers.ReviewSerializer(reviews, many=True).data
        return Response(data=data)
        
    elif request.method == 'POST':
        serializer = serializers.ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')
        
        review = models.Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id
        )
        return Response(
            data=serializers.ReviewSerializer(review).data, 
            status=status.HTTP_201_CREATED
        )


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(data={'error': 'Review not found!'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        data = serializers.ReviewSerializer(review).data
        return Response(data=data)
        
    elif request.method == 'PUT':
        serializer = serializers.ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
        review.save()
        
        return Response(
            data=serializers.ReviewSerializer(review).data, 
            status=status.HTTP_200_OK
        )
        
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def product_reviews_api_view(request):
    products = models.Product.objects.prefetch_related('reviews').annotate(rating=Avg('reviews__stars'))
    data = serializers.ProductReviewSerializer(products, many=True).data
    return Response(data=data)