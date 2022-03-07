from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from company.models import Provider
from company.serializers import ProviderSerializer


class ProviderViewSet(ModelViewSet):
    queryset = Provider.active_objects.all()
    serializer_class = ProviderSerializer

    def destroy(self, request, *args, **kwargs):
        provider = self.get_object()
        provider.remove()
        return Response(status=status.HTTP_204_NO_CONTENT)

