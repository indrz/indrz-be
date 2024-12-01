from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    dj_pass = os.getenv('DJANGO_SUPERUSER_PASSWORD')
    dj_user = os.getenv('DJANGO_SUPERUSER_USERNAME')
    dj_email = os.getenv('DJANGO_SUPERUSER_EMAIL')

    def handle(self, *args, **options):
        """
        Creates an admin user non-interactively if it doesn't exist
        """
        User = get_user_model()
        if not User.objects.filter(username=self.dj_user).exists():
            admin = User.objects.create_superuser(username=self.dj_user,
                                          email=self.dj_email,
                                          password=self.dj_pass)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            print("Done, created new Admin user")
        else:
            print("Admin user already exists")
