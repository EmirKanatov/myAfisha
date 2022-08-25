from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DirectorSerializer, MovieSerializer, MovieDetailSerializer, ReviewSerializer
from .models import Director, Movie, Review
# Create your views here.


@api_view(['GET'])
def directors_view(request):
    directors = Director.objects.all()
    serializer = DirectorSerializer(directors, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def directors_detail_view(request, id):
    directors = Director.objects.get(id=id)
    serializer = DirectorSerializer(directors)
    return Response(data=serializer.data)


@api_view(['GET'])
def movies_view(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def movies_detail_view(request, id):
    movies = Movie.objects.get(id=id)
    serializer = MovieDetailSerializer(movies)
    return Response(data=serializer.data)


@api_view(['GET'])
def reviews_view(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def reviews_detail_view(request, id):
    reviews = Review.objects.get(id=id)
    serializer = ReviewSerializer(reviews)
    return Response(data=serializer.data)


@api_view(['GET'])
def movies_reviews_view(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(data=serializer.data)
