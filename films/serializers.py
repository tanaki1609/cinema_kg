from rest_framework import serializers
from .models import Film, Director, Genre


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
    director = DirectorSerializer(many=False)
    # genres = GenreSerializer(many=True)
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = 'id title rating is_hit created director genres reviews'.split()
        depth = 1

    def get_genres(self, film):
        return film.genre_list[0:2]
