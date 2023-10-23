# Scrapper

Komenda do odpalenia: 
`scrapy crawl doniczki -o products.json`.

Dostajemy:
- folder `images`, gdzie każdy folder nazwany jest za pomocą `ID` produktu, a w środku jego zdjęcia.
- `products.json`, informacje o produktach w postaci 
```json
{  "id": value,
   "price":value,
   "name":value,
   "category":value,
   "manufacturer":value
}
```


