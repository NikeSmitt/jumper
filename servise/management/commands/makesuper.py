from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@jumper.ru', 'admin')
            self.stdout.write(self.style.SUCCESS('Admin user has created'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user already exists'))
