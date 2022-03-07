import phonenumbers
import pytest
from faker import Faker
from rest_framework.test import APIClient

from company.models import Provider

fake = Faker('IN')


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
