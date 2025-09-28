from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import time


def buy_item():
    products_available = driver.find_elements(By.CSS_SELECTOR, value='div[id="products"] div[id^="product"]')
    cookies_available = driver.find_element(By.ID, value="cookies").text
    cookies_available = int(cookies_available.split()[0])
    for product in reversed(products_available):
        if "enabled" in product.get_attribute("class"):
            try:
                product_name, price = product.text.split()
            except ValueError as msg:
                # print(msg, product.text)
                product_name, price, _ = product.text.split()
            finally:
                if int(price) < cookies_available:
                    product.click()
                    print(f"Bought item: {product.get_attribute('id')}")
                    break



chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://ozh.github.io/cookieclicker/")
driver.maximize_window()

time.sleep(2)

polski = driver.find_element(By.XPATH, value='//*[@id="langSelect-PL"]')
polski.click()
time.sleep(3)

timeout = time.time() + 5 # >> 5 seconds
time_end = time.time() + 5*60 # >> 5 minutes

cookie = driver.find_element(By.ID, value="bigCookie")
products = driver.find_elements(By.CSS_SELECTOR, value='div[id="products"] div[id^="product"]')


while True:
    cookie.click()
    if time.time() > timeout:
        buy_item()
        timeout = time.time() + 5
    if time.time() > time_end:
        break

# time.sleep(2)
try:
    cookies_per_sec = driver.find_element(By.ID, value="cookiesPerSecond")
    print(f"cookies/second: {cookies_per_sec.text.split()[2]}")
except StaleElementReferenceException:
    print("Coudn't find cookies/second object...")

time.sleep(5)

driver.quit()
# cookies/second: 16.6 original
