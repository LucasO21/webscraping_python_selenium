
# Imports
import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Setup
driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
url    = "https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc"
driver.get(url)
WDW(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="ja-current-content"]/div[2]/div[2]/div/div[3]/div/div[1]')))

# - Functions
def scroll_to_bottom():
    
    # - Grab The Height of The Page
    last_height = driver.execute_script('return document.body.scrollHeight')

    # - Scroll To The Bottom of The Page
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
    
# ---------------------------------------------------------------------------------------------------------------------------------------------

# GET LINKS FOR ALL VEHICLES

links_list = []

while True:
    
    # - Scroll to buttom
    scroll_to_bottom()
    
    # - Get urls of vehicles and append to list
    try:
        # - Grab HTML
        soup = BS(driver.page_source, 'lxml')

        # - Grab links
        posting_card = soup.find_all('div', class_ = lambda x: x and x.startswith('item_'))

        for post in posting_card:
            link = post.find('a', class_ = 'product-item-link')['href']
            links_list.append(link)        
    except:
        pass
    
    # - Click on the next page
    try:
        next_button = driver.find_element('xpath', '//*[@id="ja-current-content"]/div[2]/div[2]/div/div[2]/div/div[1]/ul/li[9]/a/span')
        next_button.click()        
        WDW(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="ja-current-content"]/div[2]/div[2]/div/div[3]/div/div[1]/a/div')))
    except:
        break

driver.quit()


# - Save Dataframe
links_list_final = []

for i in links_list:
    full_link = 'https://www.gtabase.com/' + i
    links_list_final.append(full_link)
    
df_links = pd.DataFrame({'vehicle_links': links_list_final})

df_links.to_csv(r'data/gtabase/vehicle_links.csv', index=False)



