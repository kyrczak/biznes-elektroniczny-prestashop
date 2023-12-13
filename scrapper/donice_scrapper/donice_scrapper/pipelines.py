# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import time
import os
class DoniceScrapperPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
         
         for image_url in item['image_urls']:
            path = os.path.splitext(image_url)[0]
            filename = os.path.basename(path)
            yield Request(image_url, meta={'item': item, 'filename': filename})
        

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        image_guid = item['id']
        timestamp = int(time.time())
        return f'{image_guid}/{request.meta["filename"]}.jpg'
    

    
    def item_completed(self, results, item, info):
        return item