from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.contrib.gis.geos import Point

from company.models import Provider, ServiceArea
from company.serializers import ProviderSerializer, ServiceAreaSerializer


class ProviderViewSet(ModelViewSet):
    queryset = Provider.active_objects.all()
    serializer_class = ProviderSerializer

    def destroy(self, request, *args, **kwargs):
        provider = self.get_object()
        provider.remove()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceAreaViewSet(ModelViewSet):
    queryset = ServiceArea.active_objects.all()
    serializer_class = ServiceAreaSerializer

    def destroy(self, request, *args, **kwargs):
        service_area = self.get_object()
        service_area.remove()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def find(self, request, *args, **kwargs):
        """
        This is used to query saved polygon using a lat/lng combination
        (should be provided by a query param).
        """
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')

        if not all([lat, lng]):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"msg": "lat/lng pair should be provided"})

        try:
            lat = float(lat)
            lng = float(lng)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"msg": "lat/lng should be numbers."})

        pnt = Point(x=lat, y=lng)

        service_areas = ServiceArea.active_objects.filter(poly__contains=pnt).all()
        serializer = self.get_serializer(service_areas, many=True)
        return Response(data=serializer.data)
