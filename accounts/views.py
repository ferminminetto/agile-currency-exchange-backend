from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.contrib.auth.models import User

from .models import Account
from .serializers import AccountSerializer, UserSerializer, AccountLogSerializer
from currencies.models import Currency


class AccountGetDataTemplate(views.APIView):

    def get(self, request, *args, **kwargs):
        try:
            account = Account.objects.get(owner__id=kwargs.get('user_id'))
            if account.owner_id != request.user.id:
                raise PermissionDenied
            return Response(self.to_serialize(account), status=status.HTTP_200_OK)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AccountGetData(AccountGetDataTemplate):

        def to_serialize(self, account):
            serializer = AccountSerializer(account, many=False)
            return serializer.data


class AccountLogsGetData(AccountGetDataTemplate):

    def to_serialize(self, account):
        serializer = AccountLogSerializer(account.logs, many=True)
        return serializer.data


class OperateAccountWithMoney(views.APIView):

    # This method must be overriden by the subclasses
    def operation_with_money(self, request):
        pass

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        account = Account.objects.select_for_update().get(id=kwargs.get('account_id'))
        try:
            if account.owner_id != request.user.id:
                raise PermissionDenied
            self.operation_with_money(request, account)
            return Response(status=status.HTTP_200_OK)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AccountAddMoney(OperateAccountWithMoney):

    def operation_with_money(self, request, account):
        account.add_money(float(request.data.get('value_to_add')))


class AccountWithdrawMoney(OperateAccountWithMoney):

    def operation_with_money(self, request, account):
        account.withdraw_money(float(request.data.get('value_to_withdraw')))


class AccountTransferMoney(OperateAccountWithMoney):

    def operation_with_money(self, request, account):
        value_to_transfer = float(request.data.get('value_to_transfer'))
        account_to_transfer_id = int(request.data.get('account_to_transfer_id'))
        account_to_transfer = Account.objects.select_for_update().get(id=account_to_transfer_id)
        account.transfer_money(value_to_transfer, account_to_transfer)


class UserGetData(views.APIView):

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('user_id'))
            if user.id != request.user.id:
                raise PermissionDenied
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)


class RegisterUser(views.APIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if not request.data['currency_id']:
            raise ValidationError({'currency': 'You need to select a currency to associate to your account'})

        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_created = user_serializer.create(user_serializer.data)
        user_created.is_active = True
        user_created.set_password(user_serializer.data['password'])
        user_created.save()

        currency = Currency.objects.get(id=int(request.data['currency_id']))
        account = Account.objects.create(
            balance=0.0, owner=user_created, currency=currency
        )
        return Response(status=status.HTTP_201_CREATED)
