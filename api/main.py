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
        if category_id == "1" or category_id == "2":
            continue
        category_delete_url = API_DEFAULT_LINK + f'categories/{category_id}?ws_key={API_KEY}'
        delete_response = requests.delete(category_delete_url)

        if delete_response.status_code == 200 or delete_response.status_code == 404:
            print(f"Category {category_id} deleted successfully.")

def remove_products():
    import requests

    # Get the list of categories
    products_url = API_DEFAULT_LINK + 'products' + f'?ws_key={API_KEY}'
    response = requests.get(products_url)
    root = fromstring(response.content)

    product_ids = [product.get('id') for product in root.findall('.//product')]
    print(product_ids)
    # Iterate through the category IDs and delete each one
    for product_id in product_ids:
        product_delete_url = API_DEFAULT_LINK + f'products/{product_id}?ws_key={API_KEY}'
        delete_response = requests.delete(product_delete_url)
        print(delete_response.status_code)
        if delete_response.status_code == 200 or delete_response.status_code == 404:
            print(f"product {product_id} deleted successfully.")


    
def add_category(category_name, parent_id=None):
    category_schema["category"]["name"]["language"]["value"] = category_name
    category_schema["category"]["active"] = 1
    category_schema["category"]["id_parent"] = parent_id
    category_schema["category"]["link_rewrite"]["language"]["value"] = category_name.lower().replace(" ", "-")
    category_schema["category"]["description"]["language"]["value"] = f'Produkty z kategorii {category_name}'
    return prestashop.add('categories', category_schema)["prestashop"]["category"]["id"]
def get_category_id(category_name):
    return prestashop.get('categories', options={'filter[name]': category_name})["categories"]["category"]["attrs"]["id"]

def convert_price_to_float(price):
    tax = 1.23
    return round(float(price.replace(",", ".").replace("zł", "").replace(" ","").replace("\xa0","").strip())/tax,2)

def add_product(product):
    
    #DATA
    product_schema["product"]["reference"] = product["id"]
    product_schema["product"]["id_category_default"] = get_category_id(product["category"])
    product_schema["product"]["name"]["language"]["value"] = product["name"]
    product_schema["product"]["associations"]["categories"] = {
            "category": [
                {"id": 2},
                {"id": get_category_id(product["category"])}
            ],
        }
    product_schema["product"]["price"] = convert_price_to_float(product["price"])
    print(product_schema["product"]["price"])
    product_schema["product"]["link_rewrite"]["language"]["value"] = product["name"].lower().replace(" ", "-")
    product_schema["product"]["meta_title"]["language"]["value"] = product["name"]
    if product["attributes"]["weight"] is None:
        product_schema["product"]["weight"] = 0.5
    else:
        product_schema["product"]["weight"] = product["attributes"]["weight"]
    product_schema["product"]["description_short"]["language"]["value"] = product["short_description"]
    product_schema["product"]["description"]["language"]["value"] = f'{product["short_description"]}<br><strong>Masa:</strong> {product["attributes"]["weight"]}g<br><strong>Producent:</strong> {product["manufacturer"]}'

    #OPTIONS
    product_schema["product"]["id_tax_rules_group"] = 1
    product_schema["product"]["active"] = 1
    product_schema["product"]["state"] = 1
    product_schema["product"]["available_for_order"] = 1
    product_schema["product"]["minimal_quantity"] = 1
    product_schema["product"]["show_price"] = 1
    product_schema["product"]["id_shop_default"] = 1


    prestashop.add("products", product_schema)["prestashop"]["product"]["id"]



def process_categories():
    try:
        with open('./categories.json', 'r') as json_file:
            categories_data = json.load(json_file)
    except:
        print("Problem z categories.json")
        return

    main_site_category_index = 2
    #print categories and their subcategories
    for main_category, subcategories in categories_data.items():
        print(main_category)
        parent_id = add_category(main_category, 2)
        for subcategory in subcategories:
            print(subcategory)
            add_category(subcategory, parent_id)
        

        
def process_products(products_data):
    
    try:
        with open('./products.json', 'r') as json_file:
            products_data = json.load(json_file)
    except:
        print("Problem z products.json")
        return
        
    cnt = 0
    for product in products_data:
        prod ={
            "id": product["id"],
            "price": product["price"],
            "name": product["name"],
            "short_description": product["short_description"],
            "category": product["category"],
            "attributes": product["attributes"],
            "manufacturer": product["manufacturer"],
        }
        print("Adding product: ", prod["name"])
        cnt += 1
        add_product(prod)






if __name__ == "__main__":
    
    prestashop = prestapyt.PrestaShopWebServiceDict(
        API_DEFAULT_LINK, API_KEY)

    remove_categories()
    remove_products()

    category_schema = prestashop.get('categories', options={'schema': 'blank'})
    product_schema = prestashop.get('products', options={'schema': 'blank'})
    del product_schema["product"]["position_in_category"]
    del product_schema["product"]["associations"]["combinations"]


    #process_categories()
    #process_products()
