from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.contrib.auth.models import User

from .models import Account
from .serializers import AccountSerializer, UserSerializer


class AccountGetData(views.APIView):

    def get(self, request, *args, **kwargs):
        try:
            account = Account.objects.get(id=kwargs.get('account_id'))
            if account.owner_id != request.user.id:
                raise PermissionDenied
            serializer = AccountSerializer(account, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)


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
        account.add_money(float(request.POST.get('value_to_add')))


class AccountWithdrawMoney(OperateAccountWithMoney):

    def operation_with_money(self, request, account):
        account.withdraw_money(float(request.POST.get('value_to_withdraw')))


class AccountTransferMoney(OperateAccountWithMoney):

    def operation_with_money(self, request, account):
        value_to_transfer = float(request.POST.get('value_to_transfer'))
        account_to_transfer_id = int(request.POST.get('account_to_transfer_id'))
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
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.create(user_serializer.data)
        return Response(status=status.HTTP_201_CREATED)
