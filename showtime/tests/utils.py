from random import sample, randint, choice

import pytz
from faker import Faker

from Cinemas.settings import TIME_ZONE
from movielist.models import Movie
from showtime.models import Cinema, Screening

faker = Faker("pl_PL")
T_ZONE = pytz.timezone(TIME_ZONE)


def random_movies():
    ''' Return random movies '''
    movies = list(Movie.objects.all())
    return sample(movies, 3)


def add_screening_fake(cinema):
    '''add 3 screening for given cinema'''
    movies = random_movies()
    for movie in movies:
        Screening.objects.create(cinema=cinema, movie=movie, date=faker.date_time(T_ZONE))


def fake_cinema_data():
    return {
        "name": faker.name(),
        "city": faker.city(),
    }


def create_fake_cinema():
    cinema = Cinema.objects.create(**fake_cinema_data())
    add_screening_fake(cinema)
