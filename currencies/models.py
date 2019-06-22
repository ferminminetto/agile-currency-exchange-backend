from django.db import models
from common.BaseModel import BaseModel


class Currency(BaseModel):

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    symbol = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    name_plural = models.CharField(max_length=100)
    decimal_digits = models.IntegerField()

    is_master = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    exchange_rate = models.FloatField(default=0.0000000)

    def __str__(self):
        return '%s - %s' % (self.code, self.name)

    def value_equivalence_to_other_currency(self, other_currency_value, other_currency_exchange_rate):
        """
        Used if I want to convert a value from another currency to my currency value
        """
        master_currency_value = other_currency_value * other_currency_exchange_rate
        return master_currency_value / self.exchange_rate
