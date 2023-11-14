from const import *
import prestapyt

# Create categories

# Create products

if __name__ == "__main__":
    pshop = prestapyt.PrestaShopWebServiceDict(
        API_DEFAULT_LINK, API_KEY)
    
    categories_schema = pshop.get('categories', 
                           options={
                               'schema': 'blank'
                               })
    
    proudcts_schema = pshop.get('products', 
                           options={
                               'schema': 'blank'
                               })
    
    #print(categories_schema)
    #print(products_schema)


    