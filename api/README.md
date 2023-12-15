# API
Detailed info about accessing API through website.

## Libraries
The API script use `prestapyt` library to access Prestashop API. It is installed automatically with `requirements.txt` file.
## API KEY
`6MG3TTH9HV43IJU2B7K6AJUQBQCVHERI`

## API access
`http://localhost:8080/api`

Username: `API KEY`

## Add new category
To manually add new category you need to attach it to the end of `../results/categories.json` file in following format:
```json
    "Category Name"{
        "Subcategory Name": "Subcategory URL",
        //...
                   },
        //...

```
## Add new product
To manually add new product you need to attach it to the end of `../results/products.json` file in following format:
```json
    {
        "id": "value",
        "price": "value zł",
        "name": "value",
        "short_description": "value",
        "category": "value",
        "attributes": {
            "material": ["value1",
                         "value2",
                         "value3"],
            "amount": "value",
            "weight": "value",
            //additional attributes
            "additional_attribute1": "value",
            "additional_attribute": "value",
            "additional_attribute3": "value",

        },
        "manufacturer": "value",
        "image_urls": [
            "url1",
            "url2",
        ],
        "full_description": //...
    },

```
