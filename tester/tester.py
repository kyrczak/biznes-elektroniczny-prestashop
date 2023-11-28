from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random


driver = webdriver.Chrome()

driver.get("http://localhost:8080")

def back():
    driver.navigate().back()

def get_categories():
    main_categories = driver.find_elements(by=By.XPATH, value="//ul[@id='top-menu']/child::*")
    main_categories = [ x for x in main_categories if x.text != "STRONA GŁÓWNA" ]
    return main_categories

def get_subcategories(category):
    category.find_elements(by=By.XPATH, value="./div/ul/li")

def get_products(driver):
    return driver.find_elements(by=By.XPATH, value="//div[@class='thumbnail-top']")

def hover(element):
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()

def get_next_page_btn():
    btn = driver.find_element(by=By.XPATH, value="//a[@rel='next']")
    return btn
def next_page():
    try:
        btn = get_next_page_btn()
        driver.get(btn.get_attribute('href'))
    except:
        pass


def add_product():
    ##on category screen
    products = driver.find_elements(by=By.XPATH, value="//div[@class='thumbnail-top']")
    selected_product = random.choice(products)
    selected_product.click()
    driver.implicitly_wait(2)
    #set_quantity
    add_to_cart = driver.find_element(by=By.XPATH, value="//button[contains(@class, 'add-to-cart')]")
    if(not add_to_cart.is_enabled):
        categoryOptions[-2].click() ## go back
        return
    quantity_input = driver.find_element(by=By.ID, value="quantity_wanted")
    quantity = random.randrange(1,10)
    quantity_input.click()
    quantity_input.send_keys(Keys.BACKSPACE) 
    quantity_input.send_keys(str(quantity)) ##enter number of products
    add_to_cart.click() ##added product to the cart     
    #time.sleep(1)
    #driver.find_element(by=By.XPATH, value="//div[@class='cart-content-btn']/button[@class='btn btn-secondary']").click() ##close 'added to cart' screen
    categoryOptions = driver.find_elements(by=By.XPATH, value="//nav[@class='breadcrumb hidden-sm-down']/ol/li")
    categoryOptions[-2].click() ## go back
    driver.implicitly_wait(2)

def element_exists(method, val):
    try:
        driver.find_element(by=method, value=val)
    except BaseException:
        return False
    return True

def product_available():
    if(element_exists(method=By.ID, val='product-availability')):
        elem = driver.get_element(by=By.ID, value='product-availability')
        if elem.text == 'Obecnie brak na stanie':
            return False
    return True

def select_category(main = 1, sub = 1):
    ##on any screen
    categories = get_categories()
    category = categories[main]
    hover(category)
    driver.implicitly_wait(2)
    subcategories = category.find_elements(by=By.XPATH, value="./div/ul/li")
    subcategory = subcategories[sub]
    subcategory.click()
    driver.implicitly_wait(2)



##ADDING PRODUCTS
def add_products():
    select_category(0,2)
    #add 3 products from this page
    for _ in range(3):
        add_product()
    for _ in range(3):
        next_page()
        #input('...')
        driver.implicitly_wait(2)
        add_product()

    select_category(1,1)
    for _ in range(3):
        add_product()
    for _ in range(3):
        next_page()
        driver.implicitly_wait(2)
        add_product()

    select_category(3,3)
    for _ in range(3):
        add_product()
    for _ in range(3):
        next_page()
        driver.implicitly_wait(2)
        add_product()

def search_and_add():
    ##search for products
    searchTerm = "konewka"
    driver.get("http://localhost:8080")
    search_bar = driver.find_element(by=By.XPATH, value="//input[@class='ui-autocomplete-input']")
    search_bar.click()
    search_bar.send_keys(searchTerm)
    search_bar.send_keys(Keys.RETURN)
    add_product()


##enter cart
driver.get("http://localhost:8080")
cart = driver.find_element(by=By.ID, value="_desktop_cart")
if cart.is_enabled:
    cart_url = cart.find_element(by=By.XPATH, value="//a").get_attribute("href")
    print(cart_url)
    driver.get(cart_url)

input("...")

driver.quit()
