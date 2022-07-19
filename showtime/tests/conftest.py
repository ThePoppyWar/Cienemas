import os

import pytest
from rest_framework.test import APIClient

from showtime.models import Cinema

@pytest.fixture
def client():
    client = APIClient()
    return client

# @pytest.fixture
# def set_up():
#     for _ in range(5):
#         Cinema.objects.create(name=)