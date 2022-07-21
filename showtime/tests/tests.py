import pytest as pytest
import pytz

from faker import Faker

from Cinemas.settings import TIME_ZONE
from movielist.models import Movie
from showtime.models import Cinema, Screening
from .utils import fake_cinema_data

faker = Faker("pl_PL")
T_ZONE = pytz.timezone(TIME_ZONE)


@pytest.mark.django_db
def test_add_cinema(client, set_up):
    cinemas = Cinema.objects.count()
    new_cinema = fake_cinema_data()
    response = client.post("/cinemas/", new_cinema, format='json')
    assert response.status_code == 201
    assert Cinema.objects.count() == cinemas + 1
    for key, value in new_cinema.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_add_screening(client, set_up):
    screenings = Screening.objects.count()
    new_screening_data = {
        'cinema': Cinema.objects.first().name,
        "movie": Movie.objects.first().title,
        "date": faker.date_time(tzinfo=T_ZONE).isoformat()
    }
    response = client.post("/screening/", new_screening_data, format="json")
    assert response.status_code == 201
    assert Screening.objects.count() == screenings + 1

    new_screening_data["date"] = new_screening_data["date"].replace("+00:00", "Z")
    for key, value in new_screening_data.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_get_cinema_list(client, set_up):
    response = client.get("/cinemas/", {}, format='json')

    assert response.status_code == 200
    assert Cinema.objects.count() == len(response.data)


def test_get_screening_list(client, set_up):
    response = client.get("/screening/", {}, format="json")

    assert response.status_code == 200
    assert Screening.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_cinema_detail(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f"/cinemas/{cinema.id}/", {}, format='json')

    assert response.status_code == 200
    for field in ("name", "city", "movies"):
        assert field in response.data


@pytest.mark.django_db
def test_get_screening_detail(client, set_up):
    screening = Screening.objects.first()
    response = client.get(f"/screenings/{screening.id}/", {}, format="json")

    assert response.status_code == 200
    for field in ('movie', "cinema", "date"):
        assert field in response.data


@pytest.mark.django_db
def test_delete_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.delete(f"cinemas/{cinema.id}/", {}, format='json')
    assert response.status_code == 204
    cinema_ids = [cinema.id for cinema in Cinema.objects.all()]
    assert cinema.id not in cinema_ids


@pytest.mark.django_db
def test_delete_screening(client, set_up):
    screening = Screening.objects.first()
    response = client.delete(f"/screenings/{screening.id}", {}, format='json')
    assert response.status_code == 204
    screening_ids = [screening.id for screening in Screening.objects.all()]
    assert screening.id not in screening_ids


@pytest.mark.django_db
def test_update_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f"/cinemas/{cinema.id}/", {}, format='json')
    cinema_data = response.data
    new_name = "MC"
    cinema_data["name"] = new_name
    response = client.patch(f"/cinemas/{cinema.id}/", cinema_data, format='json')
    assert response.status_code == 200
    cinema_obj = Cinema.objects.get(id=cinema.id)
    assert cinema_obj.name == new_name


@pytest.mark.django_db
def test_update_screening(client, set_up):
    screening = Screening.objects.first()
    response = client.get(f"/screenings/{screening.id}", {}, format='json')
    screening_data = response.data
    new_cinema = Cinema.objects.last()
    screening_data['cinema'] = new_cinema.name
    response = client.patch(f'/screenings/{screening.id}/', screening_data, format="json")
    assert response.status_code == 200
    screening_obj = Screening.objects.get(id=screening.id)
    assert screening_obj.cinema == new_cinema
