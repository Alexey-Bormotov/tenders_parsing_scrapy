from django.core.management.base import BaseCommand

from web_app.models import (
    JuridicalPerson, Region, Tender, TenderItem, TenderType
)


class Command(BaseCommand):
    help = 'Очистка базы данных тендеров'

    def handle(self, *args, **options):
        """ Очистка базы данных. """

        print('Запуск очистки базы данных.')
        JuridicalPerson.objects.all().delete()
        Region.objects.all().delete()
        Tender.objects.all().delete()
        TenderItem.objects.all().delete()
        TenderType.objects.all().delete()
        print('База данных очищена.')
