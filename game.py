from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import time


def buy_item():
    products_dict = {
        "ids": [],
        "names": [],
        "prices": []
    }
    products_available = driver.find_elements(By.CSS_SELECTOR, value=".enabled")
    for product in products_available:
        try:
            text = product.text
        except:
            print(f"SOMETHIN with {product}")
        else:
            if text != '' and text != 'Wycisz':
                try:
                    product_name, price = product.text.split()
                except ValueError as msg:
                    # print(msg, product.text)
                    product_name, price, _ = product.text.split()
                finally:
                    products_dict["ids"].append(product.get_attribute("id"))
                    products_dict["names"].append(product_name)
                    products_dict["prices"].append(int(price))
                    # print(product_name, price)
                # product_name = product.find_element(By.CLASS_NAME, value="title.productName")
                # product_price = product.find_element(By.CLASS_NAME, value=".price")
                # print(product_price,product_name)

    if products_dict["prices"]:
        the_most_expensive = max(products_dict['prices'])
        expensive_idx = products_dict["prices"].index(the_most_expensive)
        expensive_label = products_dict["ids"][expensive_idx]
        cookies = driver.find_element(By.ID, value="cookies").text
        cookies_count = int(cookies.split()[0])
        if cookies_count > the_most_expensive:
            buy_object = driver.find_element(By.ID, value=f"{expensive_label}")
            buy_object.click()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://ozh.github.io/cookieclicker/")
driver.maximize_window()


time.sleep(2)

# add_ons = driver.find_element(By.CLASS_NAME, value="cc_btn cc_btn_accept_all")
# add_ons.click()

polski = driver.find_element(By.XPATH, value='//*[@id="langSelect-PL"]')
polski.click()
time.sleep(3)

timeout = time.time() + 5 # >> 5 seconds
time_end = time.time() + 5*60 # >> 5 minutes

cookie = driver.find_element(By.ID, value="bigCookie")
# cursor = driver.find_element(By.)
# cookie.click()
# time.sleep(3)
while True:
    cookie.click()
    if time.time() > timeout:
        buy_item()
        timeout = time.time() + 5
        # print(time.time())
        # print(time_end)
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

# cookies/second: 9.1 bez timeout refresh()
# cookies/second: 14.5 timetout refresh()