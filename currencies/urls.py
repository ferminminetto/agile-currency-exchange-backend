from django.urls import path, include
from rest_framework import routers
from .views import CurrencyViewSet

router = routers.DefaultRouter()
router.register('currencies', CurrencyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]