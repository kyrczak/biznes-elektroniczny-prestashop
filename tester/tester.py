from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import calendar
import random

options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')

driver = webdriver.Chrome(options=options)

driver.get("https://localhost:8080")

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


def add_product_s():
    timeout = 1
    ##on category screen
    products = driver.find_elements(by=By.XPATH, value="//div[@class='thumbnail-top']")
    selected_product = random.choice(products)
    try:
        selected_product.click()
    except:
        print("product unavailable")
        return

    driver.implicitly_wait(0.5)
    #set_quantity
    add_to_cart = driver.find_element(by=By.XPATH, value="//button[contains(@class, 'add-to-cart')]")
    if(not add_to_cart.is_enabled):
        print("button was inactive at the beginning")
        #categoryOptions[-2].click() ## go back
        return
    
    quantity = random.randrange(1,5)
    
    for i in range(quantity):
       ##added product to the cart
        print(i)
        try:
            WebDriverWait(driver,timeout).until(EC.staleness_of(add_to_cart))
            add_to_cart = driver.find_element(by=By.XPATH, value="//button[contains(@class, 'add-to-cart')]")
        except:
            pass
        try:
            add_to_cart = driver.find_element(by=By.XPATH, value="//button[contains(@class, 'add-to-cart')]")
            
            WebDriverWait(driver,timeout).until(EC.element_to_be_clickable(add_to_cart))
        except:
            print("button didn't become active")
            break
        add_to_cart.click()
        try:
            WebDriverWait(driver,timeout+1).until(EC.presence_of_element_located((By.XPATH,"//div[@class='cart-content-btn']/button")))
        except:
            print("continue btn does not exist")
            break
        
        continue_shopping = driver.find_element(by=By.XPATH, value="//div[@class='cart-content-btn']/button")
        if(i != 0):
            try:
                WebDriverWait(driver,timeout+1).until(EC.staleness_of(continue_shopping))
                continue_shopping = driver.find_element(by=By.XPATH, value="//div[@class='cart-content-btn']/button")
            except:
                pass
        try:
            WebDriverWait(driver,timeout+1).until(EC.element_to_be_clickable(continue_shopping))
        except:
            print("continue btn unavailavle")
            break
        continue_shopping.click()


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
def add_products(full = False):
    select_category(0,2)
    driver.implicitly_wait(2)
    products_url = driver.current_url
    print(products_url)
    
    #add 3 products from this page
    for _ in range(3):
        add_product_s()
        driver.get(products_url)
        driver.implicitly_wait(2)
    
    if(full == False):
        return
    
    next_page()
    driver.implicitly_wait(2)
    products_url = driver.current_url
    for _ in range(3):
        add_product_s()
        driver.get(products_url)
        driver.implicitly_wait(2)

    select_category(1,1)
    driver.implicitly_wait(2)
    products_url = driver.current_url
    for _ in range(3):
        add_product_s()
        driver.get(products_url)
        driver.implicitly_wait(2)
    
    next_page()
    driver.implicitly_wait(2)
    products_url = driver.current_url
    for _ in range(3):
        add_product_s()
        driver.get(products_url)
        driver.implicitly_wait(2)

    select_category(3,3)
    driver.implicitly_wait(2)
    products_url = driver.current_url
    for _ in range(3):
        add_product_s()
        driver.get(products_url)
        driver.implicitly_wait(2)

    next_page()
    driver.implicitly_wait(2)
    products_url = driver.current_url
    for _ in range(3):
        add_product_s()
        driver.get(products_url)
        driver.implicitly_wait(2)

def search_and_add():
    ##search for products
    searchTerm = "konewka"
    driver.get("https://localhost:8080")
    search_bar = driver.find_element(by=By.XPATH, value="//input[@class='ui-autocomplete-input']")
    search_bar.click()
    search_bar.send_keys(searchTerm)
    search_bar.send_keys(Keys.RETURN)
    add_product_s()


def edit_cart():
    ##enter cart
    driver.get("https://localhost:8080")
    cart = driver.find_element(by=By.ID, value="_desktop_cart")
    if cart.is_enabled:
        cart_url = cart.find_element(by=By.XPATH, value=".//a").get_attribute('href')
        driver.get(cart_url)

        ##in cart
        for i in range(3):
            time.sleep(1)
            delete_btns = driver.find_elements(by=By.XPATH, value="//a[@class='remove-from-cart']")
            print("BTNS COUNT = " + str(len(delete_btns)))
            if(len(delete_btns)>1):
                btn_to_click = random.choice(delete_btns)
                btn_to_click.click()
            #driver.get(cart_url)

def register():
    with open('imiona.csv') as names:
        with open('nazwiska.csv') as surnames:
            name = random.choice(names.readlines()[:500]).split(',')[0].lower().capitalize()
            surname = random.choice(surnames.readlines()[:500]).split(',')[0].lower().capitalize()
            print(name, surname)
            mail = name + '.' + surname + '@student.debil.pl'
            #mail = 'beprojekteti@outlook.com'
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
            driver.find_element(by=By.XPATH, value="//button[@name='continue']").click()

def enter_address():
    timeout = 1
    
    address_input = driver.find_element(by=By.ID, value='field-address1')
    code_input = driver.find_element(by=By.ID, value='field-postcode')
    city_input = driver.find_element(by=By.ID, value='field-city')
    city='Wolne Miasto Gdańsk'
    addr='ul. Gdyńska 1'
    postcode = '80-340'
    address_input.click()
    address_input.send_keys(addr)
    city_input.click()
    city_input.send_keys(city)
    code_input.click()
    code_input.send_keys(postcode)

    next = driver.find_element(by=By.XPATH, value="//button[@name='confirm-addresses']")
    next.click()

    ##select delivery option
    driver.implicitly_wait(1)
    input('...')
    delivery_options=driver.find_elements(by=By.XPATH, value="//input[contains(@id,'delivery_option')]")

    delivery = random.choice(delivery_options)
    try:
        delivery.click()
    except:pass
    driver.find_element(by=By.XPATH, value="//button[@name='confirmDeliveryOption']").click()
    driver.implicitly_wait(1)
    payment = driver.find_element(by=By.XPATH, value="//input[@id='payment-option-2']")
    #WebDriverWait(driver,timeout).until(EC.element_to_be_clickable(payment))
    #input('....')
    payment.click()
    driver.find_element(by=By.ID, value='conditions_to_approve[terms-and-conditions]').click()
    driver.implicitly_wait(1)
    confirm_order = driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Złóż zamówienie')]")
    confirm_order.click()

def place_order():
    ##order
    driver.get("https://localhost:8080")
    cart = driver.find_element(by=By.ID, value="_desktop_cart")
    if cart.is_enabled:
        cart_url = cart.find_element(by=By.XPATH, value=".//a").get_attribute('href')
        driver.get(cart_url)
    ##in cart
    order_btn = driver.find_element(by=By.XPATH, value="//div[@class='card cart-summary']//a[@class='btn btn-primary']")
    order_btn.click()
    driver.implicitly_wait(2)
    register()
    enter_address()

def check_order():
    ##check order status & get invoice
    driver.find_element(by=By.XPATH, value="//a[@class='account']").click()
    driver.implicitly_wait(1)
    driver.find_element(by=By.ID, value="history-link").click()
    driver.implicitly_wait(1)
    driver.find_element(by=By.XPATH, value="//a[@data-link-action='view-order-details']").click()

    #mail = 'beprojekteti@outlook.com'
    #passwd = 'biznesproj23'
    driver.implicitly_wait(2)
    driver.find_element(by=By.XPATH, value="//a[contains(text(), 'Pobierz fakturę')]").click()

add_products(full=True)
search_and_add()
edit_cart()
place_order()
check_order()
input("...")

driver.quit()
