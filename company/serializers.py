from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from company.models import Provider, ServiceArea


class ProviderSerializer(ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = Provider
        fields = (
            'id', 'name', 'email', 'phone_number', 'language', 'currency', 'status',
            'create_date', 'update_date'
        )


class ServiceAreaSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = ServiceArea
        geo_field = 'poly'
        fields = ('id', 'provider', 'name', 'price', 'poly')
