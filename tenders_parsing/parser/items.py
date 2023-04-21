import scrapy


class ParserItem(scrapy.Item):
    number = scrapy.Field()
    tender_type = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    organizer = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    object_type = scrapy.Field()
    customer = scrapy.Field()
    region = scrapy.Field()
    tender_items = scrapy.Field()
