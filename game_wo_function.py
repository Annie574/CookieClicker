from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://ozh.github.io/cookieclicker/")
driver.maximize_window()

time.sleep(2)

polski = driver.find_element(By.XPATH, value='//*[@id="langSelect-PL"]')
polski.click()
time.sleep(3)

buy_time = 5
timeout = time.time() + buy_time # >> 5 seconds
time_end = time.time() + 5*60 # >> 5 minutes

cookie = driver.find_element(By.ID, value="bigCookie")

while True:
    cookie.click()
    if time.time() > timeout:
        products_available = driver.find_elements(By.CSS_SELECTOR, value='div[id="products"] div[id^="product"]')
        cookies_available = driver.find_element(By.ID, value="cookies").text
        cookies_available = int(cookies_available.split()[0])
        for product in reversed(products_available):
            if "enabled" in product.get_attribute("class"):
                try:
                    product_name, price = product.text.split()
                except ValueError:
                    product_name, price, _ = product.text.split()
                finally:
                    #This try-except block is slowing down algo, as if item is enabled then you can afford it, right?
                    # No need to check it twice.
                    if int(price) < cookies_available:
                        product.click()
                        print(f"Bought item: {product.get_attribute('id')}")
                        break

        timeout = time.time() + buy_time
    if time.time() > time_end:
        try:
            cookies_per_sec = driver.find_element(By.ID, value="cookiesPerSecond")
            print(f"cookies/second: {cookies_per_sec.text.split()[2]}")
        except StaleElementReferenceException:
            print("Coudn't find cookies/second object...")
        break



time.sleep(5)

driver.quit()
# cookies/second: 17.8/18.8 mine
# cookies/second: 17.9/17.8 Angela's
# It's OK.
# buy_item() function slows down to 16.6 which is not bad result, yet without function is better