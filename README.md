# Doncie Hermiony - Prestashop store project
College project for "Electronic Business" course. The goal was to create a store using Prestashop with scrapped products from a real web store.

The products and images were gathered from [https://www.sklep-kwiecisty.pl/](https://www.sklep-kwiecisty.pl/). The data and images were scrapped using Scrapy. The data was then imported to Prestashop using a custom Python script.
The website was deployed using Docker and tested on Linux (WSL Ubuntu) with Selenium.

# Table of contents
- [Docker images](#docker-images)
- [Tech stack](#tech-stack)
- [Run website](#run-website)
  - [Admin panel](#admin-panel)
- [Backup](#backup)
    - [Backup scripts](#backup-scripts)
    - [Get backup](#get-backup)
    - [Save backup](#save-backup)
- [Scrapper](#scrapper)
    - [Run scrapper](#run-scrapper)
    - [Scrapper output](#scrapper-output)
- [API](#api)
    - [Run API](#run-api)
- [Selenium tests](#selenium-tests)
    - [Run tests](#run-tests)

## Docker images

Below are the docker images used in the project:\
`prestashop 1.7.8.10-apache`,
\
`mariadb:10`

# Tech stack
- Linux
- Docker
- Prestashop
- MariaDB
- Python 3
- Scrapy
- Selenium


# Run website
1. Go to `shop` folder
2. Generate SSL certificate:
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout prestashop.key -out prestashop.crt -subj "/C=PL/ST=Pomeranian Voivodeship/L=Gdansk/O=Donice Hermiony/OU=Donice Hermiony/CN=localhost"
```
3. Run containers with docker-compose:
```c++
//Linux
docker-compose up 
//Windows
docker compose up 
```
The website should be available at `https://localhost`. You will have to accept the certificate at first run.


To stop the website use:
```c++
//Linux
docker-compose down
//Windows
docker compose down
```
## Admin panel
To access admin panel go to ` https://localhost/admin1` and log in with:
```
login: beprojeteti@outlook.com
password: biznesproj23
```

# Backup
## Backup scripts
The backup scripts are prepared for Linux. 

The newest backup is available [here](https://drive.google.com/file/d/1v7w9ODVk16-KHR9Bfs86ffNNIsG1xg9z/view?usp=sharing).

## Get backup
To restore the backup stop the website and put the backup archive in `scripts/backups/` folder (only one backup file should be in the folder), go to `scripts` folder and run:
```bash
./get_backup.sh
```
The script replaces the database entrypoint and prestashop folder with the ones from the backup.

After the script finishes, start the website again.

## Save backup
To save the backup the website must be running.

Go to `scripts` folder and run:
```bash
./save_backup.sh
```
The script will ask you for the backup name. The backup will be saved in `scripts/backups/` folder with a timestamp in the name as a tar archive.

# Scrapper

Scrapper let you download products and categories from [https://www.sklep-kwiecisty.pl/](https://www.sklep-kwiecisty.pl/) and save them in json files.

To run scrapper you need to have Python.

## Run scrapper
To run scrapper go to `scrapper` folder and create virtual environment:
```bash
python3 -m venv venv
```
Then activate it:
```bash
source venv/bin/activate
```
Install dependencies:
```python
pip install -r requirements.txt
```
Run scrapper from `scrapper/donice_scrapper` folder:
```bash
cd ./scrapper/donice_scrapper
scrapy crawl categories 
scrapy crawl products
```

## Scrapper output
The scrapper will create two json files in `./results` folder:
- `categories.json` - contains all categories and subcategories from the website
- `products.json` - contains all products from the website

Additionally, the scrapper will create a folder `./results/images` with all product images. Each product will have its own folder with images named after the product id.

# API

The API let you import products and categories to Prestashop through a python script.

To run the script you need to have Python.

## Run API
To run API go to `api` folder and create virtual environment:
```bash
python3 -m venv venv
```
Then activate it:
```bash
source venv/bin/activate
```

Install dependencies:
```python
pip install -r requirements.txt
```

Run API from main folder with:
```bash
python3 ./api/main.py
```

The `./api/const.py` file contains the API url and credentials.

# Selenium tests

To run Selenium tests you need to have Python and Chrome browser.

## Run tests

To run tests go to `tester` folder and create virtual environment:
```bash
python3 -m venv venv
```
Then activate it:
```bash
source venv/bin/activate
```

Install dependencies:
```python
pip install -r requirements.txt
```

Run tests from tester folder with:
```bash
cd ./tester
python3 ./tester.py
```

# Authors

- [Tomasz Krezymon](https://github.com/komeg1)
- [Patryk Korczak](https://github.com/kyrczak)
- [Julia Chomicka](https://github.com/jvlkaa)
- [Robert Kalinowski](https://github.com/kalinovsk1)
- [Mikołaj Storoniak](https://github.com/MikoStoro)

# Additional info
Logo, banners and some of the descriptions such as Return Policy, Contact Us etc. were generated with ChatGPT and DALL-E 3.