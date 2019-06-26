from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, AccountLog
from django.core.validators import validate_email


class AccountSerializer(serializers.HyperlinkedModelSerializer):

    currency = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'balance', 'currency')

    def get_currency(self, obj):
        return obj.currency.as_json()


class AccountLogSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AccountLog
        fields = (
            'id', 'value_modified_sender', 'value_modified_receiver',
            'account_new_value', 'transaction_type'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'password'
        )

    def validate_email(self, email):
        try:
            validate_email(email)
            return email
        except:
            raise serializers.ValidationError('Please enter a valid email')

    def length_validator(self, value, name):
        if value:
            if len(value) < 5:
                raise serializers.ValidationError('Please enter a longer %s' % (name))
            else:
                return value

    def validate_username(self, username):
        return self.length_validator(username, 'username')

    def validate_password(self, password):
        return self.length_validator(password, 'password')

