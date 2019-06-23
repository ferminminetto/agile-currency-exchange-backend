from django.contrib import admin
from .models import Account, AccountLog

admin.site.register(Account)
admin.site.register(AccountLog)
