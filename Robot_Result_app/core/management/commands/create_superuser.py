from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser if one does not exist'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Superuser username')
        parser.add_argument('password', type=str, help='Superuser password')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(username,'admin@example.com', password)
            self.stdout.write(self.style.SUCCESS('Successfully created a new superuser'))
        else:
            self.stdout.write(self.style.SUCCESS('A superuser already exists'))
