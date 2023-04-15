import re
import scrapy

from urllib.parse import urljoin

from parser.config import (
    BASE_URL,
    MAX_PRICE_URL,
    MIN_PRICE_URL,
    PRICE_STEP
)

class TenderSpider(scrapy.Spider):
    name = 'tender'
    allowed_domains = ['www.etp-ets.ru']
    min_price = 0
    max_price = 0

    def get_min_max_price(self, response):
        """ Парсинг минимальной и максимальной цен. """

        selector = (
            'table tbody tr td.row-contract_start_price'
            '.sortable.sortable::text'
        )
        price = float(re.sub(r'[^\d,.]', '', response.css(selector).get()))
        if not self.min_price:
            self.min_price = price
        else:
            self.max_price = price

    def start_requests(self):
        """ Подготовка к парсингу. """

        for url in (MIN_PRICE_URL, MAX_PRICE_URL):
            yield scrapy.Request(
                url=urljoin(BASE_URL, url),
                callback=self.get_min_max_price
            )
        start_url = urljoin(
            BASE_URL,
            f'?&qs-contract_start_price-from={self.min_price}'
            f'&qs-contract_start_price-to={self.min_price + PRICE_STEP}&q=&'
        )
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        """ Основной метод парсинга. """

        for tender in response.css('table.table-hover tbody tr'):
            print(tender.css('td::text').get())
