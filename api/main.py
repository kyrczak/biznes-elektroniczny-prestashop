from const import *
import prestapyt
import json
from xml.etree.ElementTree import fromstring
import os
import re
import io
import requests
from threading import Semaphore
from concurrent.futures import ThreadPoolExecutor

sem = Semaphore(1)

def remove_categories():
    

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
    product_schema["product"]["description"]["language"]["value"] = f'{product["full_description"]}'

    #OPTIONS
    product_schema["product"]["id_tax_rules_group"] = 1
    product_schema["product"]["active"] = 1
    product_schema["product"]["state"] = 1
    product_schema["product"]["available_for_order"] = 1
    product_schema["product"]["minimal_quantity"] = 1
    product_schema["product"]["show_price"] = 1
    product_schema["product"]["id_shop_default"] = 1

    sem.acquire()
    features = add_features(product["attributes"])
    
   
    if features is not None:
        product_schema["product"]["associations"]["product_features"]["product_feature"] = features
    sem.release()
    website_product_id = prestashop.add("products", product_schema)["prestashop"]["product"]["id"]
    add_product_images(product["id"], website_product_id)
    add_stock(website_product_id, product["attributes"]["amount"])


def add_product_images(product_imgs_dir, product_id):
    try:
        for image in os.listdir(f'{RESULTS_PATH}images/{product_imgs_dir}'):
            fd = open(f'{RESULTS_PATH}images/{product_imgs_dir}/{image}', 'rb')
            f = fd.read()
            fd.close()
            try:
                prestashop.add(f'images/products/{product_id}', files=[
                    ("image", image, f)
                ])
            except:
                print("Problem z dodaniem zdjecia, rozszrzenie: ", image.split(".")[-1])
    except:
        print("Problem z dodaniem zdjecia, folder: ", product_imgs_dir)

def add_stock(product_id, product_quantity):
    stock_schema_id = prestashop.search("stock_availables", options={
        "filter[id_product]": product_id
    })[0]
    stock_schema = prestashop.get(
        "stock_availables", resource_id=stock_schema_id)
    
    stock_schema["stock_available"]["quantity"] = product_quantity
    stock_schema["stock_available"]["depends_on_stock"] = 0
    prestashop.edit("stock_availables", stock_schema)

def process_categories():
    try:
        with open(f'{RESULTS_PATH}categories.json', 'r') as json_file:
            categories_data = json.load(json_file)
    except:
        print("Problem z categories.json")
        print(f'{RESULTS_PATH}categories.json')
        return

    main_site_category_index = 2
    #print categories and their subcategories
    for main_category, subcategories in categories_data.items():
        print(main_category)
        parent_id = add_category(main_category, 2)
        for subcategory in subcategories:
            print(subcategory)
            add_category(subcategory, parent_id)
        

        
def process_products():
    
    try:
        with open(f'{RESULTS_PATH}products.json', 'r') as json_file:
            products_data = json.load(json_file)
    except:
        print("Problem z products.json")
        return
        
    with ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(process_product, products_data)
        
def process_product(product):
    prod ={
            "id": product["id"],
            "price": product["price"],
            "name": product["name"],
            "short_description": product["short_description"],
            "category": product["category"],
            "attributes": product["attributes"],
            "manufacturer": product["manufacturer"],
            "full_description": product["full_description"]
        }
    print("Adding product: ", prod["name"])
    add_product(prod)

def add_features(product_attributes):
    feature_schema = prestashop.get("product_features", options={
            "schema": "blank"
        })
    feature_option_schema = prestashop.get("product_feature_values", options={
        "schema": "blank"
        })

    features_ids = dict()
    for feature_name, feature_value in product_attributes.items():
        print (feature_name, feature_value)
        if  feature_name == "amount" or feature_name == "material" or feature_name == "price" or feature_name == "weight":
            continue
        feature = prestashop.get("product_features", options={"filter[name]": feature_name})


        if feature["product_features"]:
            feature_id = feature["product_features"]["product_feature"]["attrs"]["id"]
        else:
            feature_schema["product_feature"]["name"]["language"]["value"] = feature_name
            feature_schema["product_feature"]["position"] = 1
            feature_id = prestashop.add("product_features", feature_schema)["prestashop"]["product_feature"]["id"]

        feature_option_schema["product_feature_value"]["id_feature"] = feature_id
        feature_option_schema["product_feature_value"]["value"]["language"]["value"] = feature_value
        feature_option_schema["product_feature_value"]["custom"] = 1
        value_id = prestashop.add("product_feature_values", feature_option_schema)["prestashop"]["product_feature_value"]["id"]
        features_ids[feature_id] = value_id


    features = []
    for feature_id, feature_value_id in features_ids.items():
                features.append({
                "id": feature_id,
                "id_feature_value": feature_value_id
            })   


    return features

def remove_features():
    # Get the list of categories
    products_url = API_DEFAULT_LINK + 'product_features' + f'?ws_key={API_KEY}'
    response = requests.get(products_url)
    root = fromstring(response.content)
    product_ids = [product.get('id') for product in root.findall('.//product_feature')]
    print(product_ids)
    # Iterate through the category IDs and delete each one
    for product_id in product_ids:
        product_delete_url = API_DEFAULT_LINK + f'product_features/{product_id}?ws_key={API_KEY}'
        delete_response = requests.delete(product_delete_url)
        print(delete_response.status_code)
        if delete_response.status_code == 200 or delete_response.status_code == 404:
            print(f"product feature {product_id} deleted successfully.")
    
    products_url = API_DEFAULT_LINK + 'product_feature_values' + f'?ws_key={API_KEY}'
    response = requests.get(products_url)
    root = fromstring(response.content)
    product_ids = [product.get('id') for product in root.findall('.//product_feature_value')]
    print(product_ids)
    # Iterate through the category IDs and delete each one
    for product_id in product_ids:
        product_delete_url = API_DEFAULT_LINK + f'product_feature_values/{product_id}?ws_key={API_KEY}'
        delete_response = requests.delete(product_delete_url)
        print(delete_response.status_code)
        if delete_response.status_code == 200 or delete_response.status_code == 404:
            print(f"product_feature_value {product_id} deleted successfully.")

        


if __name__ == "__main__":
    
    prestashop = prestapyt.PrestaShopWebServiceDict(
        API_DEFAULT_LINK, API_KEY)

    remove_categories()
    remove_products()
    remove_features()

    category_schema = prestashop.get('categories', options={'schema': 'blank'})
    product_schema = prestashop.get('products', options={'schema': 'blank'})
    del product_schema["product"]["position_in_category"]
    del product_schema["product"]["associations"]["combinations"]


    process_categories()
    process_products()