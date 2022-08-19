from django.contrib import admin
from movie_app.models import Movie, Director, Review

# Register your models here.


admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Review)
