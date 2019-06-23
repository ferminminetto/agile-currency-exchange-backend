from django.test import TestCase
from currencies.models import Currency


class CurrencyTests(TestCase):

    dollar = Currency(
        symbol='$', code='USD', name='US Dollar',
        name_plural='US dollars', decimal_digits=2,
        is_master=True, active=True, exchange_rate=1
    )
    argentine_peso = Currency(
        symbol='AR$', code='ARS', name='Argentine Peso',
        name_plural='Argentine Pesos', decimal_digits=2,
        is_master=False, active=True, exchange_rate=0.023
    )
    japanese_yen = Currency(
        symbol='¥', code='JPY', name='Japanese Yen',
        name_plural='Japanese Yen', decimal_digits=0,
        is_master=False, active=True, exchange_rate=0.0093
    )

    def test_to_string(self):
        self.assertEquals(str(self.dollar), 'USD - US Dollar')
        self.assertNotEqual(str(self.japanese_yen), '¥ - Japanese Yen')

    def test_value_equivalence_to_other_currency(self):
        to_round = self.japanese_yen.value_equivalence_to_other_currency(1, self.argentine_peso.exchange_rate)
        self.assertEquals(round(to_round, 1), 2.5)

        value_to_check = self.dollar.value_equivalence_to_other_currency(100, self.dollar.exchange_rate)
        self.assertEquals(value_to_check, 100.0)
