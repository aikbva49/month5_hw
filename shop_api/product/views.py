from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from . import serializers
from . import models 

# --- CATEGORIES (Список и Создание) ---
@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = models.Category.objects.annotate(products_count=Count('products'))
        data = serializers.CategorySerializer(categories, many=True).data
        return Response(data=data)
        
    elif request.method == 'POST':
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- CATEGORIES (Детали, Изменение, Удаление) ---
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
        serializer = serializers.CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- PRODUCTS (Список и Создание) ---
@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = models.Product.objects.select_related('category').all()
        data = serializers.ProductSerializer(products, many=True).data
        return Response(data=data)
        
    elif request.method == 'POST':
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- PRODUCTS (Детали, Изменение, Удаление) ---
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
        serializer = serializers.ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- REVIEWS (Список и Создание) ---
@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = models.Review.objects.select_related('product').all()
        data = serializers.ReviewSerializer(reviews, many=True).data
        return Response(data=data)
        
    elif request.method == 'POST':
        serializer = serializers.ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- REVIEWS (Детали, Изменение, Удаление) ---
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
        serializer = serializers.ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- PRODUCTS WITH REVIEWS & RATING (Остается только на чтение GET) ---
@api_view(['GET'])
def product_reviews_api_view(request):
    products = models.Product.objects.prefetch_related('reviews').annotate(rating=Avg('reviews__stars'))
    data = serializers.ProductReviewSerializer(products, many=True).data
    return Response(data=data)