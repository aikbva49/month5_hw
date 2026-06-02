from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from . import serializers
from . import models 

# --- CATEGORIES ---
@api_view(['GET'])
def category_list_api_view(request):
    categories = models.Category.objects.annotate(products_count=Count('products'))
    data = serializers.CategorySerializer(categories, many=True).data
    return Response(data=data)

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = models.Category.objects.annotate(products_count=Count('products')).get(id=id)
    except models.Category.DoesNotExist:
        return Response(data={'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    data = serializers.CategorySerializer(category).data
    return Response(data=data)

# --- PRODUCTS ---
@api_view(['GET'])
def product_list_api_view(request):
    products = models.Product.objects.select_related('category').all()
    data = serializers.ProductSerializer(products, many=True).data
    return Response(data=data)

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = models.Product.objects.get(id=id)
    except models.Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    data = serializers.ProductSerializer(product).data
    return Response(data=data)

# --- REVIEWS ---
@api_view(['GET'])
def review_list_api_view(request):
    reviews = models.Review.objects.select_related('product').all()
    data = serializers.ReviewSerializer(reviews, many=True).data
    return Response(data=data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(data={'error': 'Review not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    data = serializers.ReviewSerializer(review).data
    return Response(data=data)

# --- PRODUCTS WITH REVIEWS & RATING ---
@api_view(['GET'])
def product_reviews_api_view(request):
    products = models.Product.objects.prefetch_related('reviews').annotate(rating=Avg('reviews__stars'))
    data = serializers.ProductReviewSerializer(products, many=True).data
    return Response(data=data)