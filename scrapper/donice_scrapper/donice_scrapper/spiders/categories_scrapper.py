from pathlib import Path
import scrapy
import json 
import os

class CategoriesSpider(scrapy.Spider):
    name = "categories"
    start_urls = ["https://sklep-kwiecisty.pl/"]

    def parse(self, response):
        menu_list = response.css('ul.menu-list.large.standard li.parent')
        
        result = {}

        for category in menu_list:
            category_name = category.css('h3 a::attr(title)').get()
            if category_name is None:
                continue
            category_link = category.css('a').xpath('@href').get()
        
            subcategories = category.css('div.submenu.level1 ul.level1 li p a::attr(title)').getall()
            subcategory_links = category.css('div.submenu.level1 ul.level1 li p a::attr(href)').getall()

            result[category_name] = {subcategories[i]: response.urljoin(subcategory_links[i]) for i in range(len(subcategories))}


        if not os.path.exists('../results'):
            os.makedirs('../results')
            
        with open('../results/categories.json', 'w') as json_file:
            json.dump(result, json_file, indent=4,ensure_ascii=False)