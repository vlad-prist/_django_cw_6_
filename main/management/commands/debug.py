from django.core.management import BaseCommand

from main.models import Message, Client, Settings
from main.services.sending import send_email


class Command(BaseCommand):
    help = 'Runs APScheduler.'

    def handle(self, *args, **options):
        message_client = Client.objects.get(pk=1)
        message_settings = Settings.objects.get(pk=7)
        send_email(message_client, message_settings)

