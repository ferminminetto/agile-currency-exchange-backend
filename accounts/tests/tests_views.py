from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .tests_models import AccountAndAccountLogBaseTestCase
from accounts.models import Account
from django.contrib.auth.models import User


class AccountViewsTests(AccountAndAccountLogBaseTestCase, APITestCase):

    def test_get_account_info(self):
        account = Account.objects.first()
        response = self.client.get(reverse('account_get_data', kwargs={
            'user_id': account.owner.id,
        }))
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        token = 'Bearer ' + self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('account_get_data', kwargs={
            'user_id': account.owner.id,
        }))
        self.assertEquals(response.data['balance'], 100.0)

    def test_add_money_in_account(self):
        account_id = Account.objects.first().id
        token = 'Bearer ' + self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        response = self.client.post(reverse('account_add_money', kwargs={
            'account_id': account_id,
        }), {'value_to_add': 50.0})
        self.assertEquals(Account.objects.first().balance, 150)

    def test_withdraw_money_in_account(self):
        account = Account.objects.first()
        account.balance = 100.0
        account.save()
        token = 'Bearer ' + self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        response = self.client.post(reverse('account_withdraw_money', kwargs={
            'account_id': account.id,
        }), {'value_to_withdraw': 50})
        self.assertEquals(Account.objects.first().balance, 50.0)

    def test_transfer_money(self):
        self.pesos_test_account.balance = 200.0
        self.dollars_test_account.balance = 0.0
        self.pesos_test_account.save()
        self.dollars_test_account.save()

        token = 'Bearer ' + self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        response = self.client.post(reverse('account_transfer_money', kwargs={
            'account_id': self.pesos_test_account.id,
            }), {
                'value_to_transfer': 100.0, 'account_to_transfer_id': self.dollars_test_account.id
            })
        self.assertEquals(Account.objects.get(currency__code='USD').balance, 2.3)
        self.assertEquals(Account.objects.get(currency__code='ARS').balance, 100)


class UserViewsTests(AccountAndAccountLogBaseTestCase, APITestCase):

    def test_get_user_data(self):
        user_to_get = User.objects.get(username='test111')

        token = 'Bearer ' + self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        response = self.client.get(reverse('user_get_data', kwargs={
            'user_id': user_to_get.id,
        }))
        self.assertEquals(response.data['username'], user_to_get.username)
        self.assertEquals(response.data['email'], user_to_get.email)

    def test_register_user(self):
        user_example = {
            'username': 'ferminmine',
            'first_name': 'fermin',
            'last_name': 'minetto',
            'password': 12345215251,
            'email': 'ferminmine',
            'currency_id': self.argentine_peso.id
        }
        response = self.client.post(reverse('register_user'), user_example)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_example = {
            'username': 'ferminmine',
            'first_name': 'fermin',
            'last_name': 'minetto',
            'password': 12345215251,
            'email': 'ferminmine@gmail.com',
            'currency_id': self.argentine_peso.id
        }
        response = self.client.post(reverse('register_user'), user_example)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        user_created = User.objects.get(username='ferminmine')
        self.assertEquals(user_created.first_name, 'fermin')
