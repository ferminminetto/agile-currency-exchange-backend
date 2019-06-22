from rest_framework import serializers
from .models import Currency


class CurrencySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Currency
        fields = (
            'id', 'symbol', 'code', 'name', 'name_plural',
            'decimal_digits', 'is_master', 'active', 'exchange_rate'
        )
