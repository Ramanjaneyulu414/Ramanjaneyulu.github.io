from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# Setup driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.ajio.com/men-tshirts/c/830216003"
driver.get(url)
time.sleep(5)

# Scroll to load more products
for i in range(10):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

# Product cards
products = driver.find_elements(By.CSS_SELECTOR, "div.item.rilrtl-products-list__item")

names = []
prices = []
ratings = []
links = []

for p in products:
    # Name
    try:
        name = p.find_element(By.CSS_SELECTOR, "div.brand").text + " " + \
               p.find_element(By.CSS_SELECTOR, "div.nameCls").text
    except:
        name = ""

    # Price
    try:
        price = p.find_element(By.CSS_SELECTOR, "span.price").text
    except:
        price = ""

    # Rating (optional)
    try:
        rating = p.find_element(By.CSS_SELECTOR, "div.rating").text
    except:
        rating = ""

    # Link
    try:
        link = p.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        link = ""

    if name.strip():
        names.append(name)
        prices.append(price)
        ratings.append(rating)
        links.append(link)

# Folder
if not os.path.exists("data"):
    os.makedirs("data")

# DataFrame
df = pd.DataFrame({
    "Name": names,
    "Price": prices,
    "Rating": ratings,
    "Link": links
})

df.to_csv("data/ajio_mens_tshirts.csv", index=False)

driver.quit()
print("Scraping complete! CSV generated.")


