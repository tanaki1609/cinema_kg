from rest_framework import serializers
from .models import Film, Director, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        exclude = 'birthday'.split()


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmListSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(many=False)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Film
        fields = 'id title rating created director genres'.split()
        # depth = 1
