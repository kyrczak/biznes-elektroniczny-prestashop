from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random


driver = webdriver.Chrome()

driver.get("http://localhost:8080")

def back():
    driver.execute_script("window.history.go(-1)")

def get_categories():
    main_categories = driver.find_elements(by=By.XPATH, value="//ul[@id='top-menu']/child::*")
    main_categories = [ x for x in main_categories if x.text != "STRONA GŁÓWNA" ]
    return main_categories

def get_subcategories(category):
    category.find_elements(by=By.XPATH, value="./div/ul/li")

def get_products():
    return driver.find_elements(by=By.CLASS_NAME, value="thumbnail")

def hover(element):
    hover = ActionChains(driver).move_to_element(category)
    hover.perform()

def get_next_page_btn():
    btn = driver.find_elements(by=By.XPATH, value="//a[@rel='next']")
    return btn

for elem in get_categories():
    print(elem.text)


## first category
category = get_categories()[1]

#replace time.sleep with sth less stupid
hover(category)
time.sleep(1)
subcategories = category.find_elements(by=By.XPATH, value="./div/ul/li")
for cat in subcategories:
    print(cat.text)
subcategories[2].click()
time.sleep(0.5)
#on the subcategory page

#add 3 products from this page
for i in range(3):
    products = get_products()
    selected_product = random.choice(products)
    selected_product.click()
    time.sleep(0.5)
    #set_quantity
    add_to_cart = driver.find_elements(by=By.XPATH, value="//button[@class='add-to-cart']/")
    print(add_to_cart.text)
    if(not add_to_cart.is_enabled):
        print("PRODUKT NIEDOSTĘPNY")
    quantity_input = driver.find_elements(by=By.XPATH, value="//div[@class='qty']/")














driver.quit()
