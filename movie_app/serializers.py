from django.db.models import Avg
from django.utils.dateparse import parse_duration
from rest_framework.exceptions import ValidationError

from .models import Director, Review, Movie
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = '__all__'

    def get_movies_count(self, ob):
        return len(ob.movie.all())


class MovieDetailSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()

    class Meta:
        model = Movie
        fields = 'id image title duration description director'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    review = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()
    director = DirectorSerializer()

    class Meta:
        model = Movie
        fields = 'title image duration review rating director'.split()

    def get_rating(self, ob):
        return ob.review.all().aggregate(Avg('stars'))['stars__avg']


class MovieValidateFields(serializers.Serializer):
    title = serializers.CharField(min_length=2)
    description = serializers.CharField(required=False)
    duration = serializers.DurationField(min_value=parse_duration("10:00"))
    director_id = serializers.IntegerField()

    def validate_director_id(self, director_id):
        if Director.objects.filter(id=director_id).count() == 0:
            raise ValidationError("This director does not exists")
        return director_id

    def validate_title(self, title):
        if Movie.objects.filter(title=title).count() > 0:
            raise ValidationError("Movie with this name already exists")
        return title


class MovieUpdateSerializer(MovieValidateFields):

    def validate_title(self, title):
        movie_id = self.context.get("movie_id")
        if Movie.objects.filter(title=title).exclude(id=movie_id).count() > 0:
            raise ValidationError("movie with this name already exists")
        return title


class DirectorValidateFields(serializers.Serializer):
    name = serializers.CharField(min_length=2)

    def validate_name(self, name):
        if Director.objects.filter(name=name).count() > 0:
            raise ValidationError("Director with this name is already exists")
        return name


class ReviewValidateFields(serializers.Serializer):
    text = serializers.CharField()
    movie = serializers.IntegerField()
    stars = serializers.IntegerField(max_value=5, min_value=1)

    def validate_movie(self, movie):
        if Movie.objects.filter(id=movie).count() == 0:
            raise ValidationError("Movie with this name does not exists")
        return movie