from pathlib import Path
import scrapy
from donice_scrapper.items import DoniceScrapperItem
class ProductSpider(scrapy.Spider):
    name = "doniczki"
    start_urls = ["https://sklep-kwiecisty.pl/doniczki/" + str(i) for i in range(1, 27)]

    def parse(self, response):
        product_links = response.css("a.prodimage.f-row").xpath("@href").extract()
        for product_link in product_links:
            yield scrapy.Request(url=response.urljoin(product_link), callback=self.parse_product)

    def parse_product(self, response):
        item = DoniceScrapperItem()
        item['id'] = response.css('input[name="product_id"]').xpath("@value").get()
        item['price'] =response.css('em.main-price::text').get()
        item['name']= response.css("title::text").get()
        item['category'] = response.css('li.bred-3 span[itemprop="name"]::text').get()
        item['manufacturer'] = response.css("a.brand").xpath("@title").get()
        image_urls = response.css("li.r--l-flex.r--l-flex-vcenter a").xpath("@href").extract()
        item["image_urls"] = ["https://sklep-kwiecisty.pl" + url for url in image_urls]
        yield item

    

    


# doniczki = response.css("div.products.products_extended.viewphot.s-row")[0]
# zdjecie = doniczki.css("span.f-grid-12.img-wrap.replace-img-list img").xpath("@data-src").get()
#ID = doniczki.css("div").xpath("@data-product-id").getall()
#Opis produktu: doniczki.css("span.productname::text").get()
#Cena: doniczki.css("div.price.f-row em::text").get()
