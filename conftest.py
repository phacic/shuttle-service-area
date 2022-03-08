import phonenumbers
import pytest
from faker import Faker
from rest_framework.test import APIClient
from django.contrib.gis.geos import GEOSGeometry

from company.models import Provider, ServiceArea

fake = Faker('IN')

POLY1 = 'POLYGON(( 10 10, 10 20, 20 20, 20 15, 10 10))'
POLY2 = 'POLYGON(( -3 -3, 7 20, 14 3, 10 15, -3 -3))'


def random_phone_number():
    while True:
        number = fake.phone_number()
        parsed_number = phonenumbers.parse(number, 'IN')
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)


@pytest.fixture()
def api_client() -> APIClient:
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture()
def gen_phone_number():
    def make_phone_number():
        return random_phone_number()

    return make_phone_number


@pytest.fixture()
def create_provider(db):
    def make_provider():
        return Provider.objects.create(
            name=fake.name(), email=fake.email, phone_number=random_phone_number(),
            language=fake.language_name(), currency=fake.currency_code()
        )

    return make_provider


@pytest.fixture()
def poly1():
    return POLY1


@pytest.fixture()
def poly2():
    return POLY2


@pytest.fixture()
def create_service_area1(db, create_provider, poly1):
    def make_service_area():
        provider = create_provider()
        poly = GEOSGeometry(poly1)
        return ServiceArea.objects.create(
            provider=provider, name=fake.name(), price=fake.pyfloat(2, 2, positive=True),
            poly=poly
        )

    return make_service_area


@pytest.fixture()
def create_service_area2(db, create_provider, poly2):
    def make_service_area():
        provider = create_provider()
        poly = GEOSGeometry(poly2)
        return ServiceArea.objects.create(
            provider=provider, name=fake.name(), price=fake.pyfloat(2, 2, positive=True),
            poly=poly
        )

    return make_service_area
