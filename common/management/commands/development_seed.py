from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from agile_currency_exchange.settings import BASE_DIR
from currencies.models import Currency
import json


def test_user_seed():
    User.objects.create_superuser('test', 'test@test.com', 'test')


def currencies_seeder(path_to_open):
    currencies_data = json.load(open(path_to_open))
    for currency_data_index in currencies_data:
        currency_data = currencies_data[currency_data_index]
        is_master = False if currency_data['code'] != 'USD' else True
        Currency.objects.create(
            symbol=currency_data['symbol'], code=currency_data['code'], name=currency_data['name'],
            name_plural=currency_data['name_plural'], decimal_digits=currency_data['decimal_digits'],
            is_master=is_master, active=is_master
        )


class Command(BaseCommand):

    def handle(self, *args, **options):
        test_user_seed()
        print('Test User created successfully!')

        path_to_open = BASE_DIR + '/common/management/commands/currencies.json'
        currencies_seeder(path_to_open)
