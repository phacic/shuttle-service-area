from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company.views import ProviderViewSet

router = DefaultRouter()
router.register(r'providers', ProviderViewSet, basename='provider')


urlpatterns = [
    path('', include(router.urls))
]
