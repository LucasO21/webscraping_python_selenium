# SCRAPE DETAILS ON GTA VEHICLES FROM GTABASE.COM

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

# - Functions ----------------------------------------------------------------------------------------------------------------------------------
def initialize_driver(url, look_xpath):
    
    driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
    url    = url
    driver.get(url)
    WDW(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, look_xpath)))
    
    


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



# ---------------------------------------------------------------------------------------------------------------------------------------------
# SCRAPE DETAILS
# ---------------------------------------------------------------------------------------------------------------------------------------------
links_list_final[0]

# - Setup
driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
url    = links_list_final[0]
driver.get(url)
WDW(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="ja-current-content"]/div[1]/div[1]/h1')))

# - Functions
def extract_subtag_text_single(tag, attribute, pattern):
    data_point = [i for i in soup.find_all(tag, attrs={attribute: True}) if pattern in i.get(attribute)][0].get(attribute).split(': ')[1]
    return data_point

def extract_subtag_text_multiple(tag, attribute, pattern):
    a_tags  = [i for i in soup.find_all(tag, attrs={attribute: True}) if pattern in i.get(attribute)]
    t_tag   = [a_tag.get(attribute) for a_tag in a_tags]
    feature = [i.replace(pattern + ':', '').strip() for i in t_tag]
    
    return feature

def extract_subspan(tag = 'dd', sub_tag = 'span',  class_1 = 'field-entry', class_2 = 'field-value', pattern = None):
    
    dd_tags = soup.find_all(tag, class_ = class_1)
                                     
    dd_data = None
    for dd in dd_tags:
        for span in dd.find_all(sub_tag):
            if span.get_text().strip() == pattern:
                dd_data = dd
                break
        if dd_data:
            break

    if dd_data:
        data = dd_data.find(sub_tag, class_= class_2).get_text().strip()     
    
    return data    

def extract_td_subtag(pattern):
    
    tr_tags = [i for i in soup.find_all('tr') if pattern in i.text]
    td_tags = [i.text.strip() for i in tr_tags] 
    data    = td_tags[0].split('\n')[1]
    
    return data

# - Scroll to buttom
scroll_to_bottom()

# - Get HTML
soup = BS(driver.page_source, 'lxml')

# - Get datapoints

# -- General Info
title            = soup.find('h1', class_ = 'contentheading').text.strip()
vehicle_class    = extract_subtag_text_single('a', 'title', 'Vehicle Class')
manufacturer     = extract_subtag_text_single('a', 'title', 'Manufacturer')
features         = extract_subtag_text_multiple('a', 'title', 'Vehicle Features')
acquisition      = extract_subtag_text_single('a', 'title', 'Acquisition')
price            = extract_subspan('dd', 'span', 'field-entry', 'field-value', 'GTA Online Price')
storage_location = extract_subtag_text_single('a', 'title', 'Storage Location')
delivery_method  = extract_subtag_text_single('a', 'title', 'Delivery Method')
modifications    = extract_subtag_text_single('a', 'title', 'Modifications')
resale_fla       = extract_subtag_text_single('a', 'title', 'Sell')
resale_price     = extract_subspan('dd', 'span', 'field-entry', 'field-value', 'Sell Price (Resale)').strip()
race_availability = extract_subtag_text_single('a', 'title', 'Race Availability')
top_speed_in_game = extract_subspan('dd', 'span', 'field-entry', 'field-value', 'Top Speed - Game Files').strip()
based_on          = extract_subspan(pattern = 'Based on (Real Life)').strip()
seats             = extract_subspan(pattern = 'Seats')
weight_in_kg      = extract_subspan(pattern = 'Mass / Weight')
drive_train       = extract_subspan(pattern = 'RWD')
gears             = extract_subspan(pattern = 'Gears')

# -- Performance (Racing)
top_speed_real    = extract_subspan(pattern = 'Top Speed - Real')
lap_time          = extract_subspan(pattern = 'Lap Time')
bulletproof       = extract_subspan(pattern = 'Bulletproof')

# -- Weapon Resistance
weapon1_resistance = extract_td_subtag(pattern = 'Homing Launcher / Oppressor Missiles / Jet Missiles')
weapon2_resistance = extract_td_subtag(pattern = 'RPG / Grenades / Sticky Bomb / MOC Cannon')
weapon3_resistance = extract_td_subtag(pattern = 'Explosive Rounds (Heavy Sniper Mk II)')
weapon4_resistance = extract_td_subtag(pattern = 'Tank Cannon (Rhino / APC)')
weapon5_resistance = extract_td_subtag(pattern = 'Anti-Aircraft Trailer Dual 20mm Flak')

# -- Statistics
speed               = soup.find('dd', class_ = 'field-entry speed').text.strip()
acceleration        = soup.find('dd', class_ = 'field-entry acceleration').text.strip()
braking             = soup.find('dd', class_ = 'field-entry braking').text.strip()
handling            = soup.find('dd', class_ = 'field-entry handling').text.strip()
overall             = soup.find('dd', class_ = 'field-entry overall').text.strip()


# ARCHIVE

# - Vehicle Class
#vehicle_class = [i for i in soup.find_all('a', attrs={"title": True}) if "Vehicle Class" in i.get('title')][0].get('title').split(': ')[1]

# - Vehicle Features
# a_tags  = [i for i in soup.find_all('a', attrs={"title": True}) if "Vehicle Features" in i.get('title')]
# t_tag   = [a_tag.get("title") for a_tag in a_tags]
# feature = [i.replace('Vehicle Features:', '') for i in t_tag]

# - Price 
# dd_tags = soup.find_all('dd', class_ = 'field-entry')

# dd_online_price = None
# for dd in dd_tags:
#     for span in dd.find_all('span'):
#         if span.get_text().strip() == 'GTA Online Price':
#             dd_online_price = dd
#             break
#     if dd_online_price:
#         break

# if dd_online_price:
#     price = dd_online_price.find('span', class_='field-value').get_text().strip()



# ---------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------