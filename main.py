from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

driver.get("https://orteil.dashnet.org/cookieclicker/")
cookie_button = driver.find_element(By.XPATH, value='//*[@id="bigCookie"]')

items = driver.find_elements(By.XPATH, value='//*[@id="products"]')
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
#five_min = time.time() + 60*5

while True:
    cookie_button.click()

    #every 5 seconds:
    if time.time() > timeout:

        #Get all upgrades:
        all_prices = driver.find_elements(By.CSS_SELECTOR, value='div#products span.price')
        item_prices = []
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.replace(",", ""))
                print(cost)
                item_prices.append(cost)


        #Dictionary of store items and prices:
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        #get current cookie count:
        money_element = driver.find_element(By.XPATH, value='//*[@id="cookies"]').text
        if "," in money_element:
            money_element = money_element.replace(',', '')

        cookie_count = int(money_element)

        #Find Upgrades That We Can Afford:
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        #Purchase most expensive affordable upgrade:
        highest_price_upgrade = max(affordable_upgrades)
        print(highest_price_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_upgrade]

        driver.find_element(By.ID, value=to_purchase_id).click()

        #Add 5 more seconds until the next check
        timeout = time.time() + 5



