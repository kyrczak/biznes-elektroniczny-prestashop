# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoniceScrapperItem(scrapy.Item):
    id = scrapy.Field()
    image_urls = scrapy.Field()
    price = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    manufacturer = scrapy.Field()
    attributes = scrapy.Field()
    short_description = scrapy.Field()
    full_description = scrapy.Field()
