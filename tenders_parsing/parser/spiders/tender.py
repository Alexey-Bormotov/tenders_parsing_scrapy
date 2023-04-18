import re
from datetime import datetime as dt
from urllib.parse import urljoin

import scrapy

from parser.config import (
    BASE_URL,
    DATETIME_FORMAT,
    MAX_PRICE_URL,
    MIN_PRICE_URL,
    PARSE_URL,
    PRICE_STEP
)
from parser.items import ParserItem


class TenderSpider(scrapy.Spider):
    name = 'tender'
    allowed_domains = ['www.etp-ets.ru']
    min_price = 0
    max_price = 0
    current_price = 0

    def get_min_max_price(self, response):
        """ Парсинг минимальной и максимальной цен. """

        selector = (
            'table tbody tr td.row-contract_start_price'
            '.sortable.sortable::text'
        )
        price = float(re.sub(r'[^\d,.]', '', response.css(selector).get()))
        if not self.min_price:
            self.current_price = self.min_price = price
        else:
            self.max_price = price

    def start_requests(self):
        """ Подготовка к парсингу. """

        for url in (MIN_PRICE_URL, MAX_PRICE_URL):
            yield scrapy.Request(
                url=urljoin(PARSE_URL, url),
                callback=self.get_min_max_price
            )
        start_url = urljoin(
            PARSE_URL,
            f'?&qs-contract_start_price-from={self.current_price}'
            f'&qs-contract_start_price-to={self.current_price + PRICE_STEP}&q=&'
        )
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        """ Основной метод парсинга. """

        for tender in response.css('table.table-hover tbody tr'):
            tender_url = tender.css(
                'td.row-procedure_name a::attr(href)'
            ).get()
            customer_url = urljoin(
                BASE_URL,
                tender.css('td.row-customer_name a::attr(href)').get()
            )
            yield response.follow(
                tender_url,
                callback=self.parse_tender,
                dont_filter=True,
                meta={'customer_url': customer_url}
            )
        next_page = urljoin(
            BASE_URL,
            response.css('ul.pagination li:contains("→") a::attr(href)').get()
        )
        # Тут он всегда будет выдавать новую страницу, надо сначала
        # проверять, спарсилась ли вторая часть ссылки. Переписать.
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            # Этот код ещё не протестирован
            self.current_price += PRICE_STEP
            new_prices_page = urljoin(
                PARSE_URL,
                f'?&qs-contract_start_price-from={self.current_price}'
                f'&qs-contract_start_price-to={self.current_price + PRICE_STEP}&q=&'
            )
            yield response.follow(new_prices_page, callback=self.parse)

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
                r'[^\d,.]',
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
