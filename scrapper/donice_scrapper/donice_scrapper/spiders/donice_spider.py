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
            '../../results/products.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
                'overwrite': True,
            },
        }
    }
    def start_requests(self):
        #fix the problem with relative paths
        with open('../../results/categories.json', 'r') as json_file:
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
        mainImg = response.css("div.mainimg img").xpath("@src").extract()[0]
        image_urls.insert(0,mainImg)

        
        #----------------------DESCRIPTION----------------------
        description = retrieve_description(response)
        item['short_description'] = description[0]
        if item['short_description'] is None:
            return
  
        item['full_description'] = (prepare_full_description(description).
                                    replace("\n", "<br><br>"))
        item['full_description'] = item['full_description'].replace("<br><br><br><br>", "<br><br>")

        if item['full_description'] is None:
            item['full_description'] = item['short_description']
        #-------------------------------------------------------
        #----------------------IMAGES---------------------------
        item['image_urls'] = ["https://sklep-kwiecisty.pl" + url for url in image_urls]
        #----------------------ATTRIBUTES-----------------------
        item['attributes'] = {}
        materials = response.xpath('//*[@id="option_7"]/option/text()').getall()

        if materials is not None:
            materials = append_additional_materials(materials)
            item['image_urls'],materials_found = find_materials_and_images(item['image_urls'],materials)
            if materials_found is not None:
                item['attributes']['material'] = materials_found
            else:
                item['attributes']['material'] = random.sample(materials,3)
        
        item['attributes']['amount'] = random.randint(0,10)
        wgt = get_weight(response, item['name'])
        item['attributes']['weight'] = wgt

        technical_data = extract_technical_data(description[1])
        if technical_data is not None:
            item['attributes'].update(technical_data)
        #-------------------------------------------------------
        

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
                targetString = "\n\n"
            case "h1":
                targetString = "\n\n"
            case "li":
                targetString = "\n- "
            case _: pass            
        responseLine = responseLine.replace(tag, targetString)

    return responseLine.strip()
   

def get_description(desription_content): #takes list of html lines from item description as an argument
    description = processLine(desription_content)
    shortDesc = description.replace('\n','.').partition('.')[0] #get first sentence
    return ( shortDesc, description )   

def retrieve_description(response):
    description_content = response.xpath('//*[@id="box_description"]/div/div//*').getall()
    description_content = response.css("div.resetcss").get()
    return get_description(description_content) # tuple: (short_description, long_description)
            
def get_weight(response, product_name):
     desc_list = response.xpath('//*[@id="box_description"]/div[2]/div//text()').getall()

     for elem in desc_list:
         if "kg" in elem.lower():
            weight_match = re.search(r'(\d[\d,\.]*)\s*kg', elem.lower())
            weight = weight_match.group(1)
            weight = float(weight.replace(',','.'))
           # print("WEIGHT:" +str(weight))
            return weight
    
    #check if product name contains weight
     if "kg" in product_name.lower():
        weight_match = re.search(r'(\d[\d,\.]*)\s*kg', product_name.lower())   
        weight = weight_match.group(1)
        weight = float(weight.replace(',','.'))  
        return weight
     
     return round(random.uniform(0.01, 5),2)

def find_materials_and_images(image_urls,materials):
    materials_found = []
    for url in image_urls:
        for material in materials:
            #change polish letters to english
            material = material.replace("ą","a")
            material = material.replace("ć","c")
            material = material.replace("ę","e")
            material = material.replace("ł","l")
            material = material.replace("ń","n")
            material = material.replace("ó","o")
            material = material.replace("ś","s")
            material = material.replace("ź","z")
            material = material.replace("ż","z")
            #add - between words
            material = material.replace(" ", "-")
            if material.lower() in url.lower():
                if material not in materials_found:
                    materials_found.append(material)

#process image urls and remove those that do not contain materials
    if len(image_urls) < 2:
        return image_urls, materials_found
    if len(materials_found) > 0:
        # keep urls that have materials in their names
        for url in image_urls:
            for material in materials_found:
                if material.lower() not in url.lower() and url in image_urls:
                        image_urls.remove(url)
                elif material.lower() in url.lower():
                    if url.endswith("webp") and url in image_urls:
                        image_urls.remove(url)
                        materials_found.remove(material)

    else:
        IMAGES_AMT_TO_KEEP = 3
        #remove all urls that end with webp
        for url in image_urls:
            if url.endswith("webp"):
                image_urls.remove(url)
        
        if len(image_urls) > IMAGES_AMT_TO_KEEP:
            image_urls = random.sample(image_urls,IMAGES_AMT_TO_KEEP)
    
    return image_urls, materials_found

def append_additional_materials(materials):
    # find materials that ends with "y" and add new material with "a" instaed of "y" at the end
    for material in materials:
        if material.endswith("y"):
            materials.append(material[:-1] + "a")
    
    #delete s2 and s3 from materials
    if "S2" in materials:
        materials.remove("S2")
    if "S3" in materials:
        materials.remove("S3")
    

    return materials

def extract_technical_data(description):
    cm_pairs = re.findall(r'(?:(?<=-)|(?<=^))\s*([^\n:]+)\s*:\s*([\d,]+\s*(?:x\s*[\d,]+)?\s*cm\.?)\s*(?:\.\n|\n|$)', description)
    liter_pairs = re.findall(r'(?:(?<=-)|(?<=^))\s*([^\n:]+)\s*:\s*([\d,]+\s*(?:l|litr|litry|litrów))\s*(?:\.\n|\n|$)', description)
    additional_pairs = re.compile(r'\s*-\s*(.*?)\s*-\s*(\d+cm)\n')
    # Combine the results from both patterns
    data_dict = {}
    for pair in cm_pairs:
        key, value = pair[:2]
        data_dict[key.strip()] = value.strip()
    for pair in liter_pairs:
        key, value = pair[:2]
        data_dict[key.strip()] = value.strip()

    # Find additional pairs
    if data_dict is not None:
        return data_dict

    for pair in additional_pairs.findall(description):
        key, value = pair[:2]
        data_dict[key.strip()] = value.strip()

def prepare_full_description(description):
    # get first three sentences from description
    full_description = description[1].split(".")
    # if there are less than 3 sentences, get all of them
    if len(full_description) < 2:
        try:
            full_description = full_description[0] + "." + full_description[1] + "."
        except:
            full_description = full_description[0]
    else:
        try: 
            full_description = full_description[0] + "." + full_description[1] + "." + full_description[2] + "." + full_description[3] + "."
        except:
            try:
                full_description = full_description[0] + "." + full_description[1] + "." + full_description[2] + "."
            except:
                full_description = full_description[0] + "." + full_description[1] + "."
    
    return full_description
    
