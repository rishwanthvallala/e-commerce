from django.core.management.base import BaseCommand
from core.models import SiteSettings

class Command(BaseCommand):
    help = "Update currency to INR in site settings"

    def handle(self, *args, **kwargs):
        settings = SiteSettings.load()
        settings.currency = "INR"
        settings.save()
        self.stdout.write(self.style.SUCCESS("Currency updated to INR"))
