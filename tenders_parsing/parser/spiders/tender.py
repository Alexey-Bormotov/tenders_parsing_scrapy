import re
from datetime import datetime as dt
from urllib.parse import urljoin

import scrapy

from parser.config import (
    BASE_URL,
    DATETIME_FORMAT,
    MAX_PRICE_URL,
    PARSE_URL,
    PRICE_CORR,
    PRICE_STEP,
    TENDERS_LIMIT
)
from parser.items import ParserItem
from web_app.models import Tender


class TenderSpider(scrapy.Spider):
    name = 'tender'
    allowed_domains = ['www.etp-ets.ru']
    current_price = max_price = 0
    full_parsing = False

    @staticmethod
    def __generate_url_with_price(price):
        """ Генерация URL адреса с заданным ценовым диапазоном. """

        return urljoin(
            PARSE_URL,
            f'?&qs-contract_start_price-from={price + PRICE_CORR}'
            f'&qs-contract_start_price-to={price + PRICE_STEP}&q='
            f'&limit={TENDERS_LIMIT}'
        )

    @staticmethod
    def __parse_tender_and_customer_url(tender):
        """ Парсинг URL для тендера и заказчика. """

        tender_url = tender.css(
            'td.row-procedure_name a::attr(href)'
        ).get()
        customer_url = urljoin(
            BASE_URL,
            tender.css('td.row-customer_name a::attr(href)').get()
        )
        return tender_url, customer_url

    @classmethod
    def __get_max_price(cls, response):
        """ Парсинг максимальной цены тендера. """

        selector = (
            'table tbody tr td.row-contract_start_price'
            '.sortable.sortable::text'
        )
        cls.max_price = float(
            re.sub(r'[^\d.]', '', response.css(selector).get())
        )

    @classmethod
    def __generate_next_page_url(cls, response):
        """ Генерация URL адреса для следующей страницы с тендерами. """

        next_page_url = response.css(
            'ul.pagination li:contains("→") a::attr(href)'
        ).get()
        if next_page_url:
            return urljoin(BASE_URL, next_page_url)
        elif cls.current_price < cls.max_price:
            cls.current_price += PRICE_STEP
            return cls.__generate_url_with_price(cls.current_price)

    def __check_tender_existence(self, tender):
        """ Проверка наличия тендера в базе данных. """

        tender_num = tender.css('td.row-procedure_number::text').get()
        if Tender.objects.filter(number=tender_num).exists():
            self.logger.info(
                f'Тендер с номером {tender_num} уже есть в базе данных'
            )
            return True

    def start_requests(self):
        """ Подготовка к парсингу. """

        yield scrapy.Request(url=MAX_PRICE_URL, callback=self.__get_max_price)
        start_url = self.__generate_url_with_price(self.current_price)
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        """ Основной метод парсинга. """

        for tender in response.css('table.table-hover tbody tr'):
            if not self.full_parsing and self.__check_tender_existence(tender):
                continue
            tender_url, customer_url = (
                self.__parse_tender_and_customer_url(tender)
            )
            yield response.follow(
                tender_url,
                callback=self.parse_tender,
                dont_filter=True,
                meta={'customer_url': customer_url}
            )
        next_page_url = self.__generate_next_page_url(response)
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_tender(self, response):
        """ Парсинг страницы тендера. """

        item = ParserItem()
        item['number'] = response.css(
            'a[id="common-info-registrationNumber"]::text'
        ).get()
        item['tender_type'] = response.css(
            'div[id="common-info-placingWay"]::text'
        ).get()
        item['title'] = response.css(
            'div[id="common-info-purchaseObjectInfo"]::text'
        ).get()
        item['price'] = float(
            re.sub(
                r'[^\d.]',
                '',
                response.css('div[id="common-info-maxSum"]::text').get())
        )
        item['organizer'] = response.css(
            'div[id=common-responsible-fullName]::text'
        ).get()
        item['start_date'] = dt.strptime(
            response.css(
                'div[id="common-datesAndVenue-publicationDateTime-element"] '
                'div div::text'
            ).get()[:16],
            DATETIME_FORMAT
        )
        item['end_date'] = dt.strptime(
            response.css(
                'div[id="common-datesAndVenue-endDate-element"] '
                'div div::text'
            ).get()[:16],
            DATETIME_FORMAT
        )
        item['object_type'] = response.css(
            'table[id="common-items"] tbody tr td div::text'
        ).get()
        yield response.follow(
            response.meta['customer_url'],
            callback=self.parse_customer,
            dont_filter=True,
            meta={'item': item}
        )

    def parse_customer(self, response):
        """ Парсинг страницы заказчика. """

        item = response.meta['item']
        item['customer'] = response.css(
            'div[id="CustomerInfo-commonInfo-fullName"]::text'
        ).get()
        item['region'] = response.css(
            'div[id="CustomerInfo-locationInfo-region"]::text'
        ).get()

        yield item
