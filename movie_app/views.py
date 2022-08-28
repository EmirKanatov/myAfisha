from django.shortcuts import render
from django.utils.dateparse import parse_duration
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DirectorSerializer, MovieSerializer, MovieDetailSerializer, ReviewSerializer
from .models import Director, Movie, Review
# Create your views here.


@api_view(['GET', 'POST'])
def directors_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        name = request.data.get("name")
        director = Director.objects.create(name=name)
        return Response(data={"message": "created",
                              "director": DirectorSerializer(director).data},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def directors_detail_view(request, id):
    try:
        directors = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={"error": "Director not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DirectorSerializer(directors)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        directors.delete()
        return Response(data={"message": "director deleted"}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        directors.name = request.data.get("name")
        directors.save()
        return Response(data={"message": "director changed"}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def movies_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)
    if request.method == 'POST':
        title = request.data.get("title")
        description = request.data.get("description")
        duration = parse_duration(request.data.get("duration"))
        director = request.data.get("director.id")
        Movie.objects.create(title=title, description=description, duration=duration, director=director)
        return Response(data={"message": "movie created"}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def movies_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MovieDetailSerializer(movie)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(data={"message": "Movie was delete"}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        movie.title = request.data.get("title")
        movie.description = request.data.get("description")
        movie.duration = parse_duration(request.data.get("duration"))
        movie.director_id = request.data.get("director_id")
        movie.save()
        return Response(data={"message": "movie was changed",
                              "movie": MovieDetailSerializer(movie).data}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def reviews_view(request):
    if request.method == "GET":
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)
    elif request.method == "POST":
        text = request.data.get("text")
        movie_id = request.data.get("movie_id")
        stars = request.data.get("stars")
        Review.objects.create(text=text, movie_id=movie_id, stars=stars)
        return Response(data={"message": "review was created"}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def reviews_detail_view(request, id):
    try:
        reviews = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReviewSerializer(reviews)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        reviews.delete()
        return Response(data={"message": "Review was deleted"}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        reviews.text = request.data.get("text")
        reviews.movie_id = request.data.get("movie_id")
        reviews.stars = request.data.get("stars")
        reviews.save()
        return Response(data={"message": "Review was changed",
                              "review": ReviewSerializer(reviews).data}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def movies_reviews_view(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(data=serializer.data)
