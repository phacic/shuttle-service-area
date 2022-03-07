from rest_framework.serializers import ModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from company.models import Provider


class ProviderSerializer(ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = Provider
        fields = (
            'id', 'name', 'email', 'phone_number', 'language', 'currency', 'status',
            'create_date', 'update_date'
        )
