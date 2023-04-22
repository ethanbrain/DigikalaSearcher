from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import urllib.request
import requests

class ProductScraper:
    
    def __init__(self, search_term):
        self.search_term = search_term
        self.driver = webdriver.Firefox()
        self.path = "assets/images/"
        
    def scrape(self):
        # OPEN SITE AND SEARCH PRODUCT ---------------------------------------------
        self.driver.get(f'https://www.digikala.com/search/?q={self.search_term}')
        self.driver.execute_script("window.scrollTo(0,3000)")

        # WAIT FOR LOAD ---------------------------------------------
        time.sleep(10)

        # DELETE OLD FILES ---------------------------------------------
        for file_name in os.listdir(self.path):
            file = self.path + file_name
            os.remove(file)
        if os.path.exists("products.txt"):
            os.remove("products.txt")
        else:
            print("File is not present in the system.")

        # SAVE PRODUCT NAME ---------------------------------------------
        names = self.driver.find_elements(By.CLASS_NAME, 'ellipsis-2')
        with open("products.txt", "w", encoding="utf-8") as f:
            for value in names:
                f.write(value.text + "\n")

        # SAVE IMAGES ---------------------------------------------
        images_div = self.driver.find_elements(By.CSS_SELECTOR,'.w-100.radius-medium.d-inline-block.lazyloaded')     
        index = 1 
        for idiv in images_div:
            src = idiv.get_attribute('src')
            img_data = requests.get(src).content
            with open(f"{self.path}image{index}.png", "wb") as f:
                f.write(img_data)
            index += 1

        # SAVE PRICE ---------------------------------------------
        price = self.driver.find_elements(By.CLASS_NAME, 'text-h5')
        with open("prices.txt", "w", encoding="utf-8") as f:
            for value in price:
                try:
                    pr = value.find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
                    f.write(pr + "\n")
                except:
                    pass

        # SAVE LINKS ---------------------------------------------
        link = self.driver.find_elements(By.CSS_SELECTOR,'.d-block.pointer.pos-relative.bg-000.overflow-hidden.grow-1.py-3.px-4.px-2-lg.h-full-md.styles_VerticalProductCard--hover__ud7aD')      
        with open("links.txt", "w", encoding="utf-8") as f:
            for value in link:
                href = value.get_attribute('href')
                f.write(href + "\n")

        # ClOSE BROWSER ---------------------------------------------
        self.driver.quit()