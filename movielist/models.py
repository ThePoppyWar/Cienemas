from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    director = models.ForeignKey(Person, related_name="movies_directed", on_delete=models.CASCADE)
    year = models.SmallIntegerField()
    actors = models.ManyToManyField(Person, related_name="movies_cast")



class Cinema(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie, through="Screening")


class Screening(models.Model):
    movie = models.ForeignKey(Movie, related_name='screening_movies', on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, related_name='screening_cinema', on_delete=models.CASCADE)
    date = models.DateTimeField()

