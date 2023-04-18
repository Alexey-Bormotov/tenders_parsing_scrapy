from scrapy.exceptions import DropItem

from web_app.models import ObjectType, Region, Tender, TenderType


class ParserPipeline:
    def process_item(self, item, spider):
        tender_type, _ = TenderType.objects.get_or_create(
            name=item['tender_type']
        )
        region, _ = Region.objects.get_or_create(name=item['region'])
        if ObjectType.objects.filter(name=item['object_type']).exists():
            object_type = ObjectType.objects.get(name=item['object_type'])
        else:
            object_type = ObjectType.objects.get(name='Не указано')

        try:
            Tender.objects.update_or_create(
                number=item['number'],
                tender_type=tender_type,
                title=item['title'],
                price=item['price'],
                organizer=item['organizer'],
                start_date=item['start_date'],
                end_date=item['end_date'],
                object_type=object_type,
                customer=item['customer'],
                region=region
            )
        except Exception as error:
            raise DropItem('Не удалось сохранить тендер в базу данных:', error)
        return item
