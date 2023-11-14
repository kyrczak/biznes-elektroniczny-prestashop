import os
import json 
import scrapy
from donice_scrapper.items import DoniceScrapperItem
import random 
import re
class ProductSpider(scrapy.Spider):
    name = "doniczki"
    #start_urls_base = ["https://sklep-kwiecisty.pl/doniczki/"]

    custom_settings={
        'FEEDS': {
            '../results/products.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
                'overwrite': True,
            },
        }
    }
    def start_requests(self):
        with open('../results/categories.json', 'r') as json_file:
            categories = json.load(json_file)

        for category in categories:
            for subcategory in categories[category]:
                yield scrapy.Request(url=categories[category][subcategory], callback=self.parse)
    
    def parse(self, response):
        product_links = response.css("a.prodimage.f-row").xpath("@href").extract()
        for product_link in product_links:
            yield scrapy.Request(url=response.urljoin(product_link), callback=self.parse_product)

    def parse_product(self, response):
        item = DoniceScrapperItem()
        item['id'] = response.css('input[name="product_id"]').xpath("@value").get()
        item['price'] =response.css('em.main-price::text').get()
        item['name']= response.css("title::text").get().replace('Sklep Kwiecisty', "")
        item['category'] = response.css('li.bred-3 span[itemprop="name"]::text').get()
        item['manufacturer'] = response.css("a.brand").xpath("@title").get()
        image_urls = response.css("div.innersmallgallery a").xpath("@href").extract()
        item['short_description'] = retrieve_description(response)
        if item['short_description'] is None:
            #skip product without description
            return
        #TODO: add full description
        item['image_urls'] = ["https://sklep-kwiecisty.pl" + url for url in image_urls][:2]
        item['attributes'] = {}
        materials = response.xpath('//*[@id="option_7"]/option/text()').getall()
        if materials is not None:
            count = len(materials)
            if count > 3:
                count = 3
            item['attributes']['material'] = random.sample(materials,count)
        item['attributes']['amount'] = random.randint(0,10)
        item['attributes']['weight'] = get_weight(response)
        yield item

   
def retrieve_description(response):
    description = response.xpath('//*[@id="box_description"]/div[2]/div/div/div[1]/text()[2]').get()
    if description is None:
        description = response.xpath('//*[@id="box_description"]/div[2]/div/p/text()').get()
    if description is None:
        description = response.xpath('//*[@id="box_description"]/div[2]/div/section/text()').get()
    
    return description
            
def get_weight(response):
     desc_list = response.xpath('//*[@id="box_description"]/div[2]/div//text()').getall()

     for elem in desc_list:
         if "kg" in elem.lower():
            weight_match = re.search(r'(\d[\d,\.]*)\s*kg', elem.lower())
            weight = weight_match.group(1)
            weight = float(weight.replace(',','.'))
            return weight
                
    

    #//*[@id="box_description"]/div[2]/div/section[1]
    
    


# doniczki = response.css("div.products.products_extended.viewphot.s-row")[0]
# zdjecie = doniczki.css("span.f-grid-12.img-wrap.replace-img-list img").xpath("@data-src").get()
#ID = doniczki.css("div").xpath("@data-product-id").getall()
#Opis produktu: doniczki.css("span.productname::text").get()
#Cena: doniczki.css("div.price.f-row em::text").get()
