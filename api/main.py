from const import *
import prestapyt
import json
from xml.etree.ElementTree import fromstring

def remove_categories():
    import requests

    # Get the list of categories
    categories_url = API_DEFAULT_LINK + 'categories' + f'?ws_key={API_KEY}'
    response = requests.get(categories_url)
    root = fromstring(response.content)

    category_ids = [category.get('id') for category in root.findall('.//category')]
    # Iterate through the category IDs and delete each one
    for category_id in category_ids:
        category_delete_url = API_DEFAULT_LINK + f'categories/{category_id}?ws_key={API_KEY}'
        delete_response = requests.delete(category_delete_url)

        if delete_response.status_code == 200 or delete_response.status_code == 404:
            print(f"Category {category_id} deleted successfully.")


    
def add_category(category_name, parent_id=None):
    category_schema["category"]["name"]["language"]["value"] = category_name
    category_schema["category"]["active"] = 1
    category_schema["category"]["id_parent"] = parent_id
    category_schema["category"]["link_rewrite"]["language"]["value"] = category_name.lower().replace(" ", "-")
    category_schema["category"]["description"]["language"]["value"] = f'Produkty z kategorii {category_name}'
    return prestashop.add('categories', category_schema)["prestashop"]["category"]["id"]
    
#def process_products(products_data):




def process_categories(categories_data):
    #print categories and their subcategories
    for main_category, subcategories in categories_data.items():
        print(main_category)
        parent_id = add_category(main_category, 1)
        for subcategory in subcategories:
            print(subcategory)
            add_category(subcategory, parent_id)
        

        







if __name__ == "__main__":
    
    prestashop = prestapyt.PrestaShopWebServiceDict(
        API_DEFAULT_LINK, API_KEY)

    with open('./api/categories.json', 'r') as json_file:
        categories_data = json.load(json_file)

    with open('./api/products.json', 'r') as json_file:
        products_data = json.load(json_file)

    #remove_categories()

    category_schema = prestashop.get('categories', options={'schema': 'blank'})

    process_categories(categories_data)
    #process_products(products_data)

    