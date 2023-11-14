# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import time

class DoniceScrapperPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print(f"Downloading images for item with ID: {item['id']} and URLs: {item['image_urls']}")
        for image_url in item['image_urls']:
           yield Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        image_guid = item['id']
        timestamp = int(time.time())
        return f'full/{image_guid}/{image_guid}_{timestamp}.jpg'
    

    
    def item_completed(self, results, item, info):
        return item