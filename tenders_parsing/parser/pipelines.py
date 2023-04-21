from scrapy.exceptions import DropItem

from web_app.models import (
    Customer, ObjectType, Organizer, Region, Tender, TenderItem, TenderType
)


class ParserPipeline:
    def process_item(self, item, spider):
        tender_type, _ = TenderType.objects.get_or_create(
            name=item['tender_type']
        )
        organizer, _ = Organizer.objects.get_or_create(name=item['organizer'])
        object_type = (
            ObjectType.objects.filter(name=item['object_type']).first()
            or ObjectType.objects.get(name='Не указано')
        )
        customer, _ = Customer.objects.get_or_create(name=item['customer'])
        region, _ = Region.objects.get_or_create(name=item['region'])
        try:
            tender, _ = Tender.objects.update_or_create(
                number=item['number'],
                tender_type=tender_type,
                title=item['title'],
                price=item['price'],
                organizer=organizer,
                start_date=item['start_date'],
                end_date=item['end_date'],
                object_type=object_type,
                customer=customer,
                region=region
            )
        except Exception as error:
            raise DropItem(
                f'Не удалось сохранить тендер c номером {item["number"]} '
                f'в базу данных: {error}'
            )
        try:
            for tender_item in item['tender_items']:
                print(tender_item)
                TenderItem.objects.create(
                    code=tender_item[0],
                    title=tender_item[1],
                    quantity=tender_item[2],
                    price=tender_item[3],
                    tender=tender
                )
        except Exception as error:
            raise DropItem(
                f'Не удалось сохранить предметы закупки/контракта для '
                f'тендера {tender} в базу данных: {error}'
            )
        return item
