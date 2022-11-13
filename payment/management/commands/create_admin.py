from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os

class Command(BaseCommand):


    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        admin_user_name = os.environ.get('admin_user_name')
        password = os.environ.get('password')
        if  User.objects.filter(username=admin_user_name).exists():
            self.stdout.write(f'Super Admin Already Exists -> {admin_user_name}')
        else:
            User.objects.create_superuser(
                username=admin_user_name,
                email='none@gmail.com',
                password=password
            )
            self.stdout.write(f'Super Admin Created Succesfull')