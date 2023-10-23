from pathlib import Path
import scrapy
from donice_scrapper.items import DoniceScrapperItem
class ProductSpider(scrapy.Spider):
    name = "doniczki"
    start_urls = ["https://sklep-kwiecisty.pl/doniczki/" + str(i) for i in range(1, 27)]

    
    def parse(self, response):
        for produkt in response.css("div.product-main-wrap"):
                item = DoniceScrapperItem()
                item['id'] = produkt.css("div").xpath("@data-product-id").get()
                item['price'] =produkt.css("div.price.f-row em::text").get()
                item['name']= produkt.css("span.productname::text").get()
                item['category'] = produkt.css("div").xpath("@data-category").get()
                item['manufacturer'] = produkt.css("div.f-row.manufacturer a.brand").xpath("@title").get()
                item["image_urls"] = ["https://sklep-kwiecisty.pl" + produkt.css("span.f-grid-12.img-wrap.replace-img-list img").xpath("@data-src").get()]
                yield item    

    

    


# doniczki = response.css("div.products.products_extended.viewphot.s-row")[0]
# zdjecie = doniczki.css("span.f-grid-12.img-wrap.replace-img-list img").xpath("@data-src").get()
#ID = doniczki.css("div").xpath("@data-product-id").getall()
#Opis produktu: doniczki.css("span.productname::text").get()
#Cena: doniczki.css("div.price.f-row em::text").get()
