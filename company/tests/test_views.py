import json
import pytest
from django.urls import reverse
from rest_framework import status
from faker import Faker
from company.models import Provider, ServiceArea
from company.utils import ActiveStatus

fake = Faker('IN')

JSON_CONTENT = "application/json"


@pytest.mark.django_db
class TestProviderView:

    def test_create_provider(self, api_client, gen_phone_number):
        url = reverse("provider-list")

        phone_number = gen_phone_number()
        data = {
            "name": fake.name(),
            "email": fake.email(),
            "phone_number": phone_number,
            "language": fake.language_name(),
            "currency": fake.currency_code(),
        }

        response = api_client.post(path=url, data=json.dumps(data), content_type=JSON_CONTENT)
        response_data = response.json()

        # return appropriate status code
        assert response.status_code == status.HTTP_201_CREATED

        provider_id = response_data['id']

        # provider should be in the db
        provider = Provider.objects.filter(id=provider_id).first()
        assert provider is not None

    def test_fetch_one_provider(self, api_client, create_provider):
        provider = create_provider()
        url = reverse("provider-detail", args=[provider.id])

        response = api_client.get(path=url)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data is not None

    def test_list_providers(self, api_client, create_provider):
        # create 2 providers
        create_provider()
        create_provider()

        url = reverse("provider-list")
        response = api_client.get(path=url)
        assert response.status_code == 200

        # return paginated response
        response_data = response.json()
        assert response_data is not None
        assert response_data.get('results') is not None

    def test_update(self, api_client, create_provider):
        provider = create_provider()

        url = reverse("provider-detail", args=[provider.id])
        new_name = fake.name()
        data = {
            "name": new_name
        }

        response = api_client.patch(path=url, data=json.dumps(data), content_type=JSON_CONTENT)
        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, api_client, create_provider):
        provider = create_provider()

        url = reverse("provider-detail", args=[provider.id])
        response = api_client.delete(path=url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # provider should exist but with a status of I (inactive)
        provider = Provider.objects.filter(id=provider.id).first()
        assert provider is not None
        assert provider.status == ActiveStatus.INACTIVE.value


@pytest.mark.django_db
class TestServiceArea:

    def test_create_service_area(self, api_client, poly2, create_provider):
        url = reverse('service-area-list')
        provider = create_provider()
        data = {
            "provider": provider.id,
            "name": fake.name(),
            "price": fake.pyfloat(2, 2, positive=True),
            "poly": poly2
        }

        response = api_client.post(path=url, data=json.dumps(data), content_type=JSON_CONTENT)
        assert response.status_code == status.HTTP_201_CREATED

    def test_fetch_service_area(self, api_client, create_service_area1):
        service_area = create_service_area1()
        url = reverse('service-area-detail', args=[service_area.id])
        response = api_client.get(path=url)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data is not None

    def test_update(self, api_client, create_service_area1):
        service_area = create_service_area1()

        url = reverse("service-area-detail", args=[service_area.id])
        new_name = fake.name()
        data = {
            "name": new_name
        }

        response = api_client.patch(path=url, data=json.dumps(data), content_type=JSON_CONTENT)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        print(response_data)
        assert response_data['properties']['name'] == new_name

    def test_delete(self, api_client, create_service_area1):
        service_area = create_service_area1()

        url = reverse("service-area-detail", args=[service_area.id])
        response = api_client.delete(path=url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # provider should exist but with a status of I (inactive)
        service_area = ServiceArea.objects.filter(id=service_area.id).first()
        assert service_area is not None
        assert service_area.status == ActiveStatus.INACTIVE.value

    def test_find(self, api_client, create_service_area1, create_service_area2):
        create_service_area2()
        create_service_area1()

        url = reverse("service-area-find") + '?lat=15&lng=17'
        response = api_client.get(path=url)
        assert response.status_code == status.HTTP_200_OK

        # Even though there are two services area created only one will match the query
        response_data = response.json()
        from pprint import pprint
        pprint(response_data)
        assert len(response_data['features']) == 1
