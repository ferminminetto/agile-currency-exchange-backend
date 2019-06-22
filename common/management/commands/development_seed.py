from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


def test_user_seed():
    User.objects.create_superuser('test', 'test@test.com', 'test')


class Command(BaseCommand):

    def handle(self, *args, **options):
        test_user_seed()
        print('Test User created successfully!')
