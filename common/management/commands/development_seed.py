from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from agile_currency_exchange.settings import BASE_DIR
from currencies.models import Currency
from accounts.models import Account
import json


def test_user_seed():
    User.objects.create_superuser('test', 'test@test.com', 'test')
    User.objects.create_user('antonio', 'antonio@test.com', 'antonio')
    User.objects.create_user('fermin', 'fermin@test.com', 'fermin')

    account1 = Account.objects.create(
        balance=60000.0, owner=User.objects.get(username='antonio'), currency=Currency.objects.get(code='JPY')
    )
    account1.add_money(70000.0)
    account2 = Account.objects.create(
        balance=30000.0, owner=User.objects.get(username='fermin'), currency=Currency.objects.get(code='ARS')
    )
    account2.add_money(5000.0)
    account2.transfer_money(3000, account1)
    account1.transfer_money(1000, account2)


def currencies_seeder(path_to_open):
    currencies_data = json.load(open(path_to_open))
    for currency_data_index in currencies_data:
        currency_data = currencies_data[currency_data_index]
        code = currency_data['code']
        is_master = False if code != 'USD' else True
        active = True if code == 'USD' or code == 'ARS' or code == 'JPY' else False
        Currency.objects.create(
            symbol=currency_data['symbol'], code=currency_data['code'], name=currency_data['name'],
            name_plural=currency_data['name_plural'], decimal_digits=currency_data['decimal_digits'],
            is_master=is_master, active=active
        )
    usd = Currency.objects.get(code='USD')
    usd.exchange_rate = 1
    usd.save()

    ars = Currency.objects.get(code='ARS')
    ars.exchange_rate = 0.023
    ars.save()

    jpy = Currency.objects.get(code='JPY')
    jpy.exchange_rate = 0.0093
    jpy.save()


class Command(BaseCommand):

    def handle(self, *args, **options):
        path_to_open = BASE_DIR + '/common/management/commands/currencies.json'
        currencies_seeder(path_to_open)

        test_user_seed()
        print('Test Users created successfully!')
