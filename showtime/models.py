from django.db import models

from movielist.models import Movie
# Create your models here.



class Cinema(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie, through="Screening")


class Screening(models.Model):
    movie = models.ForeignKey(Movie, related_name='screening_movies', on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, related_name='screening_cinema', on_delete=models.CASCADE)
    date = models.DateTimeField()
