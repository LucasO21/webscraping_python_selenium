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


# TEXT BOX INPUT

# Setup
url = "https://www.google.com/"
driver.get(url)

# - Input Text In a Searbox (Google)
box = driver.find_element("xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
box.send_keys("espnsoccernet.com")
box.send_keys(Keys.ENTER)

# - Click on Buttons (Google)
search_button = driver.find_element("xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]')
search_button.click()

link = driver.find_element("xpath", '//*[@id="rso"]/div[1]/div/div/div[1]/div/a/h3')
link = link.click()

scores = driver.find_element('xpath', '//*[@id="global-nav-secondary"]/div/ul/li[3]/a/span[1]')
scores = scores.click()

# - Taking a Screenshot 
driver.save_screenshot("sreenshot.png")

# - Taking a Screenshot (Full Example)
driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
url = "https://www.google.com/"
driver.get(url)

box = driver.find_element("xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
box.send_keys("arsenal fc")
box.send_keys(Keys.ENTER)

images_button = driver.find_element('xpath', '//*[@id="hdtb-msb"]/div[1]/div/div[3]/a').click()

driver.find_element('xpath', '//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img').screenshot('arsenal_logo.png')

# - Scrolling

# Return Height of Entire Webpage
driver.execute_script('return document.body.scrollHeight')

# Scrolls to Specific Section of Page
driver.execute_script('window.scrollTo(0, 500000)')

# Scrolls From Top to Bottom
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
   



    
    
