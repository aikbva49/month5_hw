from rest_framework import serializers
from .models import Film, Director, Genre
from rest_framework.exceptions import ValidationError


class DirectorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id first_name last_name birthday'.split()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id first_name last_name'.split()


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmListSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = 'id title rating created director genres reviews'.split()
        depth = 1

    def get_genres(self, film):
        return film.genre_list


class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=255)
    text = serializers.CharField(required=False)
    rating = serializers.FloatField(min_value=1, max_value=10)
    release_year = serializers.IntegerField()
    is_hit = serializers.BooleanField(default=True)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return director_id

    def validate_genres(self, genres):
        genres_db = Genre.objects.filter(id__in=genres)
        if len(genres_db) != len(genres):
            raise ValidationError('Genre does not exist!')
        return genres