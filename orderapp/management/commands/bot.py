import requests
from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    BASE_URL = f'https://api.telegram.org/bot{settings.BOT_TOKEN}/'
    
    def handle(self, *args, **options):
        r = requests.get(
            url=f'{self.BASE_URL}getMe'
            # headers='application/json'
        )
        
        print(r.status_code)
        print(r.content.decode())
        
        r = requests.post(
            # headers='application/json',
            url=f'{self.BASE_URL}sendMessage',
            data={
                'chat_id': 416205005,
                'text': 'Hello from Jumper'
            }
        )