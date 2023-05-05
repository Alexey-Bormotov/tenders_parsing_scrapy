from scrapy.exceptions import DropItem

from web_app.models import (
    JuridicalPerson, ObjectType, Region, Tender, TenderItem, TenderType
)


class ParserPipeline:
    """ Обработка собранной информации о тендере. """

    @staticmethod
    def __save_organizer_to_db(organizer_data):
        try:
            organizer_region, _ = Region.objects.get_or_create(
                name=organizer_data[13]
            )
            organizer, _ = JuridicalPerson.objects.update_or_create(
                inn=organizer_data[3],
                defaults={
                    "name": organizer_data[0],
                    "short_name": organizer_data[1],
                    "registration_date": organizer_data[2],
                    "ogrn": organizer_data[4],
                    "kpp": organizer_data[5],
                    "web_site": organizer_data[6],
                    "eis_number": organizer_data[7],
                    "telephone": organizer_data[8],
                    "email": organizer_data[9],
                    "fax": organizer_data[10],
                    "contact_person": organizer_data[11],
                    "address": organizer_data[12],
                    "region": organizer_region
                }
            )
        except Exception as error:
            raise DropItem(
                f'Не удалось сохранить организатора {organizer_data[1]} '
                f'с ИНН {organizer_data[3]} в базу данных: {error}'
            )
        return organizer

    @staticmethod
    def __save_customer_to_db(customer_data):
        try:
            customer_region, _ = Region.objects.get_or_create(
                name=customer_data[13]
            )
            customer, _ = JuridicalPerson.objects.update_or_create(
                inn=customer_data[3],
                defaults={
                    "name": customer_data[0],
                    "short_name": customer_data[1],
                    "registration_date": customer_data[2],
                    "ogrn": customer_data[4],
                    "kpp": customer_data[5],
                    "web_site": customer_data[6],
                    "eis_number": customer_data[7],
                    "telephone": customer_data[8],
                    "email": customer_data[9],
                    "fax": customer_data[10],
                    "contact_person": customer_data[11],
                    "address": customer_data[12],
                    "region": customer_region
                }
            )
        except Exception as error:
            raise DropItem(
                f'Не удалось сохранить заказчика {customer_data[1]} '
                f'с ИНН {customer_data[3]} в базу данных: {error}'
            )
        return customer, customer_region

    @staticmethod
    def __save_tender_to_db(
        tender_data,
        tender_type,
        object_type,
        organizer,
        customer,
        customer_region
    ):
        try:
            tender, _ = Tender.objects.update_or_create(
                number=tender_data['number'],
                defaults={
                    "tender_type": tender_type,
                    "title": tender_data['title'],
                    "price": tender_data['price'],
                    "organizer": organizer,
                    "start_date": tender_data['start_date'],
                    "end_date": tender_data['end_date'],
                    "object_type": object_type,
                    "customer": customer,
                    "customer_region": customer_region
                }
            )
        except Exception as error:
            raise DropItem(
                f'Не удалось сохранить тендер c номером '
                f'{tender_data["number"]} в базу данных: {error}'
            )
        return tender

    @staticmethod
    def __save_tender_items_to_db(tender_items_data, tender):
        try:
            TenderItem.objects.filter(tender=tender).delete()
            for tender_item in tender_items_data:
                TenderItem.objects.create(
                    code=tender_item[0] if tender_item[0] else None,
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

    def process_item(self, item, spider):
        tender_type, _ = TenderType.objects.get_or_create(
            name=item['tender_type']
        )
        object_type = ObjectType.objects.filter(
            name=item['object_type']
        ).first()
        organizer = self.__save_organizer_to_db(item['organizer'])
        customer, customer_region = self.__save_customer_to_db(
            item['customer']
        )
        tender = self.__save_tender_to_db(
            item,
            tender_type,
            object_type,
            organizer,
            customer,
            customer_region
        )
        self.__save_tender_items_to_db(item['tender_items'], tender)
        return item
