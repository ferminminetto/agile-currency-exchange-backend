from django.test import TestCase
from currencies.models import Currency
from accounts.models import Account, AccountLog
from django.contrib.auth.models import User


class AccountAndAccountLogBaseTestCase(TestCase):

    argentine_peso = Currency(
        symbol='AR$', code='ARS', name='Argentine Peso',
        name_plural='Argentine Pesos', decimal_digits=2,
        is_master=False, active=True, exchange_rate=0.023
    )
    dollar = Currency(
        symbol='$', code='USD', name='US Dollar',
        name_plural='US dollars', decimal_digits=2,
        is_master=True, active=True, exchange_rate=1
    )
    pesos_test_account = None
    dollars_test_account = None

    def setUp(self):
        User.objects.create_user('test111', 'testtt@testttt.com', 'testtttt1232').save()
        self.argentine_peso.save()
        self.dollar.save()
        self.pesos_test_account = Account.objects.create(
            balance=100.0, owner=User.objects.get(username='test111'), currency=self.argentine_peso
        )
        self.dollars_test_account = Account.objects.create(
            balance=100.0, owner=User.objects.get(username='test111'), currency=self.dollar
        )
        self.pesos_test_account.save()
        self.dollars_test_account.save()


class AccountTests(AccountAndAccountLogBaseTestCase):

    def test_to_string(self):
        self.assertEquals(str(self.pesos_test_account), 'test111 - Argentine Pesos')

    def test_add_money_to_account(self):
        self.pesos_test_account.add_money(100.0)
        self.assertEquals(self.pesos_test_account.balance, 200.0)

    def test_withdraw_money_from_account(self):
        self.pesos_test_account.balance = 100.0
        self.pesos_test_account.save()
        self.pesos_test_account.withdraw_money(50.0)
        self.assertEquals(self.pesos_test_account.balance, 50.0)
        with self.assertRaises(ValueError):
            self.pesos_test_account.withdraw_money(51.0)

    def test_transfer_money_from_account(self):
        self.pesos_test_account.balance = 100.0
        self.pesos_test_account.exchange_rate = 0.023
        self.pesos_test_account.save()
        self.dollars_test_account.balance = 0.00
        self.dollars_test_account.save()
        self.pesos_test_account.transfer_money(100, self.dollars_test_account)
        self.assertEquals(self.dollars_test_account.balance, 2.3)
        with self.assertRaises(ValueError):
            self.pesos_test_account.transfer_money(10, self.dollars_test_account)


class AccountLogTests(AccountAndAccountLogBaseTestCase):

    def test_logs_after_add_money_to_account(self):
        self.pesos_test_account.logs.all().delete()
        self.pesos_test_account.balance = 100.0
        self.pesos_test_account.add_money(100.0)
        self.assertEquals(self.pesos_test_account.logs.all()[0].transaction_type, AccountLog.INCOME)
        self.assertEquals(self.pesos_test_account.logs.all()[0].value_modified_sender, 100.0)
        self.assertEquals(self.pesos_test_account.logs.all()[0].account_new_value, 200.0)

    def test_logs_after_add_money_to_account(self):
        self.pesos_test_account.logs.all().delete()
        self.pesos_test_account.balance = 100.0
        self.pesos_test_account.withdraw_money(55.0)
        self.assertEquals(self.pesos_test_account.logs.all()[0].transaction_type, AccountLog.WITHDRAWAL)
        self.assertEquals(self.pesos_test_account.logs.all()[0].value_modified_sender, 55.0)
        self.assertEquals(self.pesos_test_account.logs.all()[0].account_new_value, 45.0)

    def test_logs_after_transfer_money_to_another_account(self):
        self.pesos_test_account.logs.all().delete()
        self.dollars_test_account.logs.all().delete()
        self.pesos_test_account.balance = 100.0
        self.dollars_test_account.balance = 1.00
        self.pesos_test_account.transfer_money(100.0, self.dollars_test_account)

        self.assertEquals(self.pesos_test_account.logs.all()[0].transaction_type, AccountLog.TRANSFER)
        self.assertEquals(self.pesos_test_account.logs.all()[0].value_modified_sender, 100.0)
        self.assertEquals(self.pesos_test_account.logs.all()[0].value_modified_receiver, 2.3)

        self.assertEquals(self.dollars_test_account.logs.all()[0].transaction_type, AccountLog.TRANSFER)
        self.assertEquals(self.dollars_test_account.logs.all()[0].value_modified_receiver, 2.3)
