from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company.views import ProviderViewSet, ServiceAreaViewSet

router = DefaultRouter()
router.register(r'providers', ProviderViewSet, basename='provider')
router.register(r'service-areas', ServiceAreaViewSet, basename='service-area')

urlpatterns = [
    path('', include(router.urls))
]
