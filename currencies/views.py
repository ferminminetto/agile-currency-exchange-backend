from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.conf import settings
from .models import Currency
from .serializers import CurrencySerializer

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CurrencyViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Currency.objects.all().filter(active=True)
    serializer_class = CurrencySerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, format=None):
        return super(viewsets.ModelViewSet, self).list(request, format)
