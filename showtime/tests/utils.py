from random import sample, randint, choice

import pytz
from faker import Faker

from Cinemas.settings import TIME_ZONE
from movielist.models import Movie
from showtime.models import Cinema, Screening

T_ZONE = pytz.timezone(TIME_ZONE)

faker = Faker("pl_PL")


def movies_fake():
    ''' Return random movies '''
    movies = list(Movie.objects.all())
    return sample(movies, 4)


def add_screening_fake(cinema):
    '''add 4 screening for given cinema'''
    movies = movies_fake()
    for movie in movies:
        Screening.objects.create(cinema=cinema, movie=movie, date=faker.date_time(T_ZONE))


def cinema_fake_data():
    cinema_data = {
        "name": faker.name(),
        "city": faker.city(),
    }

def cinema_creat_fake():
    cinema = Cinema.objects.create(**cinema_fake_data())
    add_screening_fake(cinema)