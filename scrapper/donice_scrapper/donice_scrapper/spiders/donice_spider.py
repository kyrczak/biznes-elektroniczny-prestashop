from pathlib import Path
import scrapy

class ProductSpider(scrapy.Spider):
    name = "doniczki"
    start_urls = ["https://sklep-kwiecisty.pl/doniczki/" + str(i) for i in range(1, 27)]

    def parse(self, response):
        for produkt in response.css("div.product-main-wrap"):
            yield {
                "ID": produkt.css("div").xpath("@data-product-id").get(),
                "Cena": produkt.css("div.price.f-row em::text").get(),
                "Opis": produkt.css("span.productname::text").get(),
                "zdjecie": produkt.css("span.f-grid-12.img-wrap.replace-img-list img").xpath("@data-src").get()
            }


# doniczki = response.css("div.products.products_extended.viewphot.s-row")[0]
# zdjecie = doniczki.css("span.f-grid-12.img-wrap.replace-img-list img").xpath("@data-src").get()
#ID = doniczki.css("div").xpath("@data-product-id").getall()
#Opis produktu: doniczki.css("span.productname::text").get()
#Cena: doniczki.css("div.price.f-row em::text").get()
