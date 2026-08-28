from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmListSerializer, FilmDetailSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except:
        return Response(data='Film not found!',
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = FilmDetailSerializer(film, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        film.title = request.data['title']
        film.text = request.data['text']
        film.release_year = request.data['release_year']
        film.rating = request.data['rating']
        film.is_hit = request.data['is_hit']
        film.director_id = request.data['director_id']
        film.genres.set(request.data['genres'])
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)


@api_view(['GET', 'POST'])
def film_list_create_api_view(request):
    if request.method == 'GET':
        # step 1: collect films (QuerySet)
        films = Film.objects.select_related('director').prefetch_related('genres', 'reviews').all()

        # step 2: reformat queryset to list of dictionaries (Serializer)
        list_ = FilmListSerializer(films, many=True).data

        # step 3: return response
        return Response(data=list_)
    elif request.method == 'POST':
        # step 1: receive data
        title = request.data.get('title')
        text = request.data.get('text')
        release_year = request.data.get('release_year')
        rating = request.data.get('rating')
        is_hit = request.data.get('is_hit')
        director_id = request.data.get('director_id')
        genres = request.data.get('genres')

        # step 2: create film
        film = Film.objects.create(
            title=title,
            text=text,
            release_year=release_year,
            rating=rating,
            is_hit=is_hit,
            director_id=director_id
        )
        film.genres.set(genres)
        film.save()

        # step 3: return response
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
