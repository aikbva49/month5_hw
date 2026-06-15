from rest_framework.response import Response
from rest_framework import status
from .models import Film, Genre, Director
from .serializers import (
    FilmListSerializer,
    FilmDetailSerializer,
    FilmValidateSerializer,
    GenreSerializer,
    DirectorSerializer,
    DirectorCreateSerializer
)
from django.db import transaction
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class GenreListAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CustomPagination


class GenreDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'id'


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return DirectorCreateSerializer
        return self.serializer_class


# Класс-CBV для списка фильмов и их создания
class FilmListCreateAPIView(ListCreateAPIView):
    queryset = Film.objects.select_related('director').prefetch_related('genres', 'reviews').all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FilmValidateSerializer
        return FilmListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        film = self.perform_create(serializer)
        return Response(
            status=status.HTTP_201_CREATED,
            data=FilmDetailSerializer(film).data
        )

    def perform_create(self, serializer):
        with transaction.atomic():
            genres = serializer.validated_data.pop('genres')
            film = Film.objects.create(**serializer.validated_data)
            film.genres.set(genres)
            film.save()
            return film


# Класс-CBV для детальной информации, обновления и удаления фильма
class FilmDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return FilmValidateSerializer
        return FilmDetailSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            genres = serializer.validated_data.pop('genres', None)
            for attr, value in serializer.validated_data.items():
                setattr(instance, attr, value)
            if genres is not None:
                instance.genres.set(genres)
            instance.save()

        return Response(FilmDetailSerializer(instance).data)