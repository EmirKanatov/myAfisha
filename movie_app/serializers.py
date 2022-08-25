from django.db.models import Avg

from .models import Director, Review, Movie
from rest_framework import serializers


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = '__all__'

    def get_movies_count(self, ob):
        return len(ob.movie.all())


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'title duration review rating'.split()

    def get_rating(self, ob):
        return ob.review.all().aggregate(Avg('stars'))['stars__avg']