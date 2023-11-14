# Scrapper

## Komendy:
Generuje kategorie do `results/categories.json`

`scrapy runspider categories_spider.py`,

 w postaci:

```json
{
"Kategoria1":{
"Podkategoria1": "link",
"Podkategoria2": "link"
            },
"Kategoria2":{"..."}
}
```
Generuje produkty do `results/products.json`

`scrapy runspider donice_spider.py`.

Dostajemy:
- folder `images`, gdzie każdy folder nazwany jest za pomocą `ID` produktu, a w środku jego zdjęcia.
- `products.json`, informacje o produktach

Przykład:

```json
{
    "id": "22039",
    "price": "24,59 zł",
    "name": "Podstawa pod parasol ogrodowy Umbrella Base MPKR",
    "short_description": "Gdy nadmiar słońca staje się dokuczliwy i brakuje naturalnej osłony drzew, wszechobecne parasole ożywiają prywatne ogrody i strefy publiczne, na stałe wpisując się w letni krajobraz. Tu istotna jest odpowiednio dobrana podstawa, gwarantująca nasze bezpieczeństwo i maksymalną stabilność parasola, którą to Umbrella Base zyskuje tylko po całkowitym wypełnieniu jej mieszaniną piasku i wody lub żwirem. Niezwykle trwała, wykonana z odpornego na działanie czynników atmosferycznych i wytrzymałego tworzywa. Podstawa wyposażona jest w pasujący do większości parasoli dostępnych na rynku grot do zamocowania sztyla.",
    "category": "Akcesoria i narzędzia",
    "attributes": {
        "material": [
            "Kość słoniowa",
            "lava",
            "Smooth gray"
        ],
        "amount": 9,
        "weight": null
    },
    "manufacturer": "PROSPERPLAST",
    "image_urls": [
        "https://sklep-kwiecisty.pl/environment/cache/images/0_0_productGfx_14661/Podstawa-pod-parasol-Umbrella-Base.jpg",
        "https://sklep-kwiecisty.pl/environment/cache/images/0_0_productGfx_14657/Podstawa-pod-parasol-Umbrella-Base.jpg"
    ]
},
```


