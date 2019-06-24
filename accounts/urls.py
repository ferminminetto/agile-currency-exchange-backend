from django.urls import path
from .views import AccountGetData, AccountAddMoney, AccountWithdrawMoney, AccountTransferMoney
from .views import UserGetData, RegisterUser

urlpatterns = [
    path('accounts/<int:account_id>/', AccountGetData.as_view(), name='account_get_data'),
    path('accounts/add-money/<int:account_id>/', AccountAddMoney.as_view(), name='account_add_money'),
    path('accounts/withdraw-money/<int:account_id>/', AccountWithdrawMoney.as_view(), name='account_withdraw_money'),
    path('accounts/transfer-money/<int:account_id>/', AccountTransferMoney.as_view(), name='account_transfer_money'),
    path('users/<int:user_id>/', UserGetData.as_view(), name='user_get_data'),
    path('users/', RegisterUser.as_view(), name='register_user')
]
