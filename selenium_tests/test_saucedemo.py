import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def login(driver):
    driver.get('https://www.saucedemo.com/')
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By.ID, 'password').send_keys('secret_sauce')
    driver.find_element(By.ID, 'login-button').click()

def test_login_page_title(driver):
    driver.get('https://www.saucedemo.com/')
    assert driver.title == 'Swag Labs'

def test_login_functionality(driver):
    login(driver)
    WebDriverWait(driver, 10).until(EC.url_contains('/inventory.html'))
    assert '/inventory.html' in driver.current_url

def test_add_to_cart(driver):
    login(driver)
    wait = WebDriverWait(driver, 10)
    # Use button data-test attribute which is stable
    add_cart_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="add-to-cart-sauce-labs-backpack"]')))
    add_cart_btn.click()
    cart_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'shopping_cart_badge')))
    assert cart_badge.text == '1'

def test_logout(driver):
    login(driver)
    wait = WebDriverWait(driver, 10)
    menu_button = wait.until(EC.element_to_be_clickable((By.ID, 'react-burger-menu-btn')))
    menu_button.click()
    logout_link = wait.until(EC.element_to_be_clickable((By.ID, 'logout_sidebar_link')))
    logout_link.click()
    WebDriverWait(driver, 10).until(EC.url_to_be('https://www.saucedemo.com/'))
    assert driver.current_url == 'https://www.saucedemo.com/'
