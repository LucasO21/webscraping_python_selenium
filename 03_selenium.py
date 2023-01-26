# SELENIUM TUTORIAL

# Imports
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

# # Setup
# url = "https://www.goat.com/sneakers"
# page = requests.get(url)
# soup = bs(page.text, "lxml")

# postings = soup.find_all("div", class_ = "GridStyles__GridCellWrapper-sc-1cm482p-0 biZBPm")

# title = soup.find("div", class_ = "GridCellProductInfo__Name-sc-17lfnu8-3 hfCoWX").text
# price = soup.find("div", class_ = "GridCellProductInfo__Price-sc-17lfnu8-6 gsZMPb").text


# Selenum Webdriver Setup
driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")

# Selenium Webdriver Test 

# - Goat Sneakers
driver.get("https://www.goat.com/sneakers")

# - Tech Crunch
driver.get("https://techcrunch.com/category/apps/")


# XPATH 

driver.find_element('xpath', '//*[@id="grid-body"]/div/div[1]/div[1]/a/div[1]/div[1]/div[1]').text

driver.find_element('xpath', '//*[@id="grid-body"]/div/div[1]/div[1]/a/div[1]/div[2]').text

# - Loop Through Multiple Postings
for i in range(1, 30):
    title = driver.find_element("xpath", '//*[@id="grid-body"]/div/div[1]/div['+ str(i) +']/a/div[1]/div[1]/div[1]').text
    print(title)
    
# - Loop Through Multiple Postings 2
colors = ["green", "red"]

url_list = ["https://www.goat.com/sneakers?color=" + color for color in colors]

titles_list = []

for url in url_list:
    
    driver.get(url)
    
    for i in range(1, 5):
        title = driver.find_element("xpath", '//*[@id="grid-body"]/div/div[1]/div['+ str(i) +']/a/div[1]/div[1]/div[1]').text
        titles_list.append(title)


# 
   
    
    
    
    
