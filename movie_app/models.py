from statistics import mean

from django.db import models

# Create your models here.


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField()
    director = models.ForeignKey(to=Director, null=True, on_delete=models.SET_NULL, related_name='movie')

    def __str__(self):
        return self.title


CHOICES = (
    (1, '*'),
    (2, '* *'),
    (3, '* * *'),
    (4, '* * * *'),
    (5, '* * * * *'),
)


class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    movie = models.ForeignKey(to=Movie, null=True, on_delete=models.SET_NULL, related_name='review')
    stars = models.IntegerField(default=5, choices=CHOICES)
