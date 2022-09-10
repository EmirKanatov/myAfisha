from django.shortcuts import render
from django.utils.dateparse import parse_duration
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import DirectorSerializer, MovieSerializer, MovieDetailSerializer, ReviewSerializer, \
    MovieValidateFields, MovieUpdateSerializer, DirectorValidateFields, ReviewValidateFields
from .models import Director, Movie, Review
# Create your views here.


class DirectorListAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination


class DirectorDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'


class MovieListAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination


class MovieDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


class ReviewsListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination


class ReviewDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


@api_view(['GET', 'POST'])
def directors_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = DirectorValidateFields(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={"errors": serializer.errors})
        name = serializer.validated_data("name")
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
        serializer = DirectorValidateFields(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={"errors": serializer.errors})
        directors.name = serializer.validated_data["name"]
        directors.save()
        return Response(data={"message": "director changed"}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def movies_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)
    if request.method == 'POST':
        serializer = MovieValidateFields(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={"errors": serializer.errors})
        title = serializer.validated_data.get("title")
        description = serializer.validated_data.get("description")
        duration = serializer.validated_data.get("duration")
        director_id = serializer.validated_data.get("director_id")
        Movie.objects.create(title=title, description=description, duration=duration, director_id=director_id)
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
        serializer = MovieUpdateSerializer(data=request.data,
                                         context={'movie_id': movie.id})
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={"errors": serializer.errors})
        movie.title = serializer.validated_data["title"]
        movie.description = serializer.validated_data["description"]
        movie.duration = serializer.validated_data["duration"]
        movie.director_id = serializer.validated_data["director_id"]
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
        serializer = ReviewValidateFields(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={"errors": serializer.errors})
        text = serializer.validated_data["text"]
        movie_id = serializer.validated_data["movie_id"]
        stars = serializer.validated_data["stars"]
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
