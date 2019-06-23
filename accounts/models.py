from django.db import models
from django.contrib.auth.models import User
from common.BaseModel import BaseModel
from currencies.models import Currency
import uuid


class AccountLog(BaseModel):

    class Meta:
        verbose_name = 'Account Log'
        verbose_name_plural = 'Account Logs'

    INCOME = 'income'
    TRANSFER = 'transfer'
    WITHDRAWAL = 'withdrawal'

    TRANSACTION_CHOICES = [
        (INCOME, 'income'),
        (TRANSFER, 'transfer'),
        (WITHDRAWAL, 'withdrawal'),
    ]

    value_modified_sender = models.FloatField()
    value_modified_receiver = models.FloatField(null=True)
    account_new_value = models.FloatField()
    receiver = models.ForeignKey('Account', on_delete=models.CASCADE, null=True)
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_CHOICES
    )


class Account(BaseModel):

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    balance = models.FloatField(default=0.00)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    logs = models.ManyToManyField(AccountLog, related_name='logs', blank=True)

    def __str__(self):
        return '%s - %s' % (self.owner.username, self.currency.name_plural)

    # Always execute this method inside a transactional context
    def add_money(self, value):
        self.balance = self.balance + value
        log = AccountLog(
            value_modified_sender=value,
            account_new_value=self.balance,
            transaction_type=AccountLog.INCOME,
            receiver=None
        )
        log.save()
        self.logs.add(log)
        self.save()

    # Always execute this method inside a transactional context
    def withdraw_money(self, value):
        if self.balance - value >= 0:
            self.balance = self.balance - value
            log = AccountLog(
                value_modified_sender=value,
                account_new_value=self.balance,
                transaction_type=AccountLog.WITHDRAWAL,
                receiver=None
            )
            log.save()
            self.logs.add(log)
            self.save()
        else:
            raise ValueError('Not enough money in user account')

    # Always execute this method inside a transactional context
    def transfer_money(self, value, account_to_transfer):
        if self.balance - value >= 0:
            self.balance = self.balance - value
            account_to_transfer_balance = account_to_transfer.currency.value_equivalence_to_other_currency(
                value, self.currency.exchange_rate
            )
            account_to_transfer.balance = account_to_transfer.balance + account_to_transfer_balance
            log = AccountLog(
                value_modified_sender=value,
                value_modified_receiver=account_to_transfer_balance,
                account_new_value=self.balance,
                transaction_type=AccountLog.TRANSFER,
                receiver=account_to_transfer
            )
            log.save()
            self.save()
            self.logs.add(log)
            account_to_transfer.logs.add(log)
            account_to_transfer.save()
        else:
            raise ValueError('Not enough money in user account')
