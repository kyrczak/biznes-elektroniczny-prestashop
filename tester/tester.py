from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode
import time
import calendar
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


def edit_cart():
    ##enter cart
    driver.get("http://localhost:8080")
    cart = driver.find_element(by=By.ID, value="_desktop_cart")
    if cart.is_enabled:
        cart_url = cart.find_element(by=By.XPATH, value=".//a").get_attribute('href')
        print(cart_url)
        driver.get(cart_url)
        print(cart_url)

        ##in cart
        for i in range(3):
            delete_btns = driver.find_elements(by=By.XPATH, value="//a[@class='remove-from-cart']")
            print("BTNS COUNT = " + str(len(delete_btns)))
            btn_to_click = random.choice(delete_btns)
            btn_to_click.click()
            #driver.get(cart_url)

def register():
#register
    driver.get("http://localhost:8080")
    account_url = driver.find_element(by=By.XPATH, value="//div[@class='user-info']").find_element(by=By.XPATH, value=".//a").get_attribute('href')
    print(account_url)
    driver.get(account_url)
    #on account page
    login_url = driver.find_element(by=By.XPATH, value="//div[@class='no-account']").find_element(by=By.XPATH, value = './/a').get_attribute('href')
    driver.get(login_url)
    driver.implicitly_wait(2)
    ##on registration page
    with open('imiona.csv') as names:
        with open('nazwiska.csv') as surnames:
            name = random.choice(names.readlines()[:500]).split(',')[0].lower().capitalize()
            surname = random.choice(surnames.readlines()[:500]).split(',')[0].lower().capitalize()
            print(name, surname)
            mail = name + '.' + surname + '@student.debil.pl'
            mail = unidecode(mail)
            year = random.randrange(1930, 2023)
            month = random.randrange(1,13)
            day = calendar.monthrange(year, month)[1]
            birth = str(year) + '-' + str(month) + '-' + str(day) 
            password = name + surname + str(year)

            input_name = driver.find_element(by=By.ID, value='field-firstname')
            input_name.click()
            input_name.send_keys(name)
            input_surname = driver.find_element(by=By.ID, value='field-lastname')
            input_surname.click()
            input_surname.send_keys(surname)
            input_email = driver.find_element(by=By.ID, value='field-email')
            input_email.click()
            input_email.send_keys(mail)
            input_gender = driver.find_element(by=By.ID, value='field-id_gender-1')
            input_gender.click()
            input_birth = driver.find_element(by=By.ID, value='field-birthday')
            input_birth.click()
            input_birth.send_keys(birth)
            input_password = driver.find_element(by=By.ID, value='field-password')
            input_password.click()
            input_password.send_keys(password)
            terms_checkbox = driver.find_element(by=By.XPATH, value="//input[@name='customer_privacy']")
            terms_checkbox.click()
            rodo_checkbox = driver.find_element(by=By.XPATH, value="//input[@name='psgdpr']")
            rodo_checkbox.click()

            ##submit
            driver.find_element(by=By.XPATH, value="//button[contains(@class, 'form-control-submit')]").click()
            ##on main page






#add_products()
#edit_cart()

input("...")




driver.quit()
