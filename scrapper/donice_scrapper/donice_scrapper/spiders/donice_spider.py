import os
import json 
import scrapy
from donice_scrapper.items import DoniceScrapperItem
import random 
import re
from time import *
class ProductSpider(scrapy.Spider):
    name = "doniczki"
    #start_urls_base = ["https://sklep-kwiecisty.pl/doniczki/"]
    categoriesArr = []
    pagination_urls = []
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
        #fix the problem with relative paths
        with open('../results/categories.json', 'r') as json_file:
            categories = json.load(json_file)
        #usunąć slice
        for category in categories:
            self.categoriesArr.append(category)
            for subcategory in categories[category]:
                self.categoriesArr.append(subcategory)
                print(categories[category][subcategory])
                yield scrapy.Request(url=categories[category][subcategory], callback=self.parse,meta={'subcategory': subcategory})
    
    def parse(self, response):
        if response.url not in self.pagination_urls:
            self.pagination_urls.append(response.url)
        product_links = response.css("a.prodimage.f-row").xpath("@href").extract()
        category_pages = response.css("div.paginator a::attr(href)").extract()
        # append each category_pages to self.pagination_urls
        for url in category_pages:
            if url not in self.pagination_urls:
                print("pagination url: " + url)
                self.pagination_urls.append(url)
                yield scrapy.Request(url=response.urljoin(url), callback=self.parse,meta={'subcategory': response.meta.get('subcategory')})

        for product_link in product_links:
            yield scrapy.Request(url=response.urljoin(product_link), callback=self.parse_product,meta={'subcategory': response.meta.get('subcategory')})

    def parse_product(self, response):
        item = DoniceScrapperItem()
        item['id'] = response.css('input[name="product_id"]').xpath("@value").get()
        item['price'] =response.css('em.main-price::text').get()
        item['name']= response.css("title::text").get().replace('Sklep Kwiecisty', "")
        
        #category = response.css('li.bred-3 span[itemprop="name"]::text').get()
        item['category'] = response.meta.get('subcategory')
        
        manufacturer = response.css("a.brand").xpath("@title").get()
        if manufacturer is None:
            manufacturer = "inne"
        item['manufacturer'] = manufacturer
        image_urls = response.css("div.innersmallgallery a").xpath("@href").extract()
        
        description = retrieve_description(response)
        item['short_description'] = description[0]
        if item['short_description'] is None:
            #skip product without description
            return
        item['full_description'] = description[1]
        if item['full_description'] is None:
            item['full_description'] = item['short_description']
        item['image_urls'] = ["https://sklep-kwiecisty.pl" + url for url in image_urls][:2]
        item['attributes'] = {}
        materials = response.xpath('//*[@id="option_7"]/option/text()').getall()
        if materials is not None:
            count = len(materials)
            if count > 3:
                count = 3
            item['attributes']['material'] = random.sample(materials,count)
        item['attributes']['amount'] = random.randint(0,10)
        wgt = get_weight(response)
        if wgt is None:
            wgt = round(random.uniform(0.01, 5),2) 
        item['attributes']['weight'] = wgt
        yield item

def processLine(responseLine): #takes single line as an argument
    
    responseLine = responseLine.replace('\n', "")
    responseLine = responseLine.replace('\t', "")
    responseLine = responseLine.replace('\r', "")
    responseLine = responseLine.strip()
    responseLine = responseLine.replace("  ", " ")
    tags = re.findall(r"<.+?>", responseLine)
    endTags = re.findall(r"</.+?>", responseLine)
    
    for tag in endTags: #replace all </> tags
        targetString = ""
        tagContent = tag[2:-1]
        match tagContent:
            case _: pass
        responseLine = responseLine.replace(tag, targetString)

    for tag in tags: #replace all <> tags
        tagContent = tag[1:-1]
        targetString = ""
        match tagContent:
            case "p": 
                targetString = "\n"
            case "br":
                targetString = "\n"
            case "li":
                targetString = "- "
            case _: pass            
        responseLine = responseLine.replace(tag, targetString)
    return responseLine
   

def getDescription(desription_content): #takes list of html lines from item description as an argument
    descriptionLinesList = [ processLine(line) for line in desription_content]
    descriptionLinesList = [ x for x in descriptionLinesList if not x.isspace()] #removing empty lines
    fullDesc = "".join(descriptionLinesList)
    shortDesc = descriptionLinesList[0].partition('.')[0] #get first sentence
    
    return ( shortDesc, fullDesc )   

def retrieve_description(response):
    desription_content = response.xpath('//*[@id="box_description"]/div/div//*').getall()
    return getDescription(desription_content) # tuple: (short_description, long_description)
            
def get_weight(response):
     desc_list = response.xpath('//*[@id="box_description"]/div[2]/div//text()').getall()

     for elem in desc_list:
         if "kg" in elem.lower():
            weight_match = re.search(r'(\d[\d,\.]*)\s*kg', elem.lower())
            weight = weight_match.group(1)
            weight = float(weight.replace(',','.'))
           # print("WEIGHT:" +str(weight))
            return weight
     return round(random.uniform(0.01, 5),2)

                
    

    #//*[@id="box_description"]/div[2]/div/section[1]
    
    


# doniczki = response.css("div.products.products_extended.viewphot.s-row")[0]
# zdjecie = doniczki.css("span.f-grid-12.img-wrap.replace-img-list img").xpath("@data-src").get()
#ID = doniczki.css("div").xpath("@data-product-id").getall()
#Opis produktu: doniczki.css("span.productname::text").get()
#Cena: doniczki.css("div.price.f-row em::text").get()
