from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_product(url):
    print("Scraping:", url)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)  # wait for page load

    try:
        title = driver.find_element(By.TAG_NAME, "h1").text
        price = driver.find_element(By.CSS_SELECTOR, "span.pdp-price").text
        print("Product:", title)
        print("Price:", price)
        driver.quit()
        return title, price
    except Exception as e:
        print("Scraping error:", e)
        driver.quit()
        return None