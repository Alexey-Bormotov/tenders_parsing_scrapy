from django.core.management.base import BaseCommand

from web_app.models import Region, Tender, TenderType


class Command(BaseCommand):
    help = 'Очистка базы данных тендеров'

    def handle(self, *args, **options):
        """ Очистка базы данных. """

        Region.objects.all().delete()
        Tender.objects.all().delete()
        TenderType.objects.all().delete()
