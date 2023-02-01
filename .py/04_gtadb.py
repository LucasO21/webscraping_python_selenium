# ---- SCRAPE DETAILS ON GTA VEHICLES FROM GTABASE.COM ----

# - Section 1: Scrape links to vehicles
# - Section 2: Scrape vehicle details
# - Section 3: Scrape upgrade cost. This data point was mistakenly skipped in section 2

#  ---- Imports ----
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


# ---- Setup ----
driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
url    = "https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc"
driver.get(url)
WDW(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="ja-current-content"]/div[2]/div[2]/div/div[3]/div/div[1]')))


# ---- Functions ----
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
    


# ---- SCRAPE LINKS FOR ALL VEHICLES ----

# - Loop through pages and get links for each vehicle
links_list = []

while True:
    
    # -- Scroll to buttom
    scroll_to_bottom()
    
    # -- Get urls of vehicles and append to list
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
    
    # -- Click on the next page
    try:
        next_button = driver.find_element('xpath', '//*[@id="ja-current-content"]/div[2]/div[2]/div/div[2]/div/div[1]/ul/li[9]/a/span')
        next_button.click()        
        WDW(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="ja-current-content"]/div[2]/div[2]/div/div[3]/div/div[1]/a/div')))
    except:
        break

driver.quit()


# ---- Format urls ----
links_list_final = []

for i in links_list:
    full_link = 'https://www.gtabase.com/' + i
    links_list_final.append(full_link)
    
df_links = pd.DataFrame({'vehicle_links': links_list_final})

# ---- Save Dataframe ----
df_links.to_csv(r'data/gtabase/vehicle_links.csv', index=False)



# ---- SCRAPE VEHICLE DETAILS ----
# test_list = links_list_final[0:11]
# url       = links_list_final[49]

# ---- Functions ----

# -- Run `scroll_to_bottom()` script from previous section above 

# -- Get single text from sub `title` tag
def extract_subtag_text_single(soup, tag = 'a', attribute = 'title', pattern = None):
    
    try:
        data_point = [i for i in soup.find_all(tag, attrs={attribute: True}) if pattern in i.get(attribute)][0].get(attribute).split(': ')[1]
    except:
        data_point = 'NA'
        
    return data_point

# -- Get multiple text from sub `title` tag
def extract_subtag_text_multiple(soup, tag = 'a', attribute = 'title', pattern = 'None'):
            
            try:
                a_tags  = [i for i in soup.find_all(tag, attrs={attribute: True}) if pattern in i.get(attribute)]
                t_tag   = [a_tag.get(attribute) for a_tag in a_tags]
                feature = [i.replace(pattern + ':', '').strip() for i in t_tag]
            except:
                feature = 'NA'
                
    
            return feature       
         
# -- Get text from sub `span` tag
def extract_subspan(soup, tag = 'dd', sub_tag = 'span',  class_1 = 'field-entry', class_2 = 'field-value', pattern = None):    

        dd_tags = soup.find_all(tag, class_ = class_1)
                                        
        dd_data = None
        for dd in dd_tags:
            for span in dd.find_all(sub_tag):
                if span.get_text().strip() == pattern:
                    dd_data = dd
                    break
            if dd_data:
                break
            
        for i in dd_data:
            if pattern in str(i):
                data = dd_data.find(sub_tag, class_= class_2).get_text().strip() 
                break
        else:
            data = 'NA'   
            
        return data

# -- Get text from `tr` tag
def extract_td_subtag(soup, pattern):
    
    try:
        tr_tags = [i for i in soup.find_all('tr') if pattern in i.text]
        td_tags = [i.text.strip() for i in tr_tags] 
        data    = td_tags[0].split('\n')[1]
        
    except:
        data = 'NA'
    return data

# -- Return NA for any errors
def try_except(func):
    
    try:
       output = func
    except:
        output = 'NA'
    
    return output
    
# ---- For loop to scrape data ----
# - After getting links for each vehicle, I proceeded to scrape details for each link in batches

batch = links_list_final[0:401]
batch = links_list_final[401:709]

# ---- Placeholder dataframe ----

# -- Re-run this section for each batch 
df_gta = pd.DataFrame({
    'title':[], 'vehicle_class':[], 'manufacturer':[], 'features':[], 'acquisition':[], 
    'price':[], 'storage_location':[], 'delivery_method':[], 'modifications':[], 'resale_flag':[], 
    'resale_price':[], 'race_availability':[], 'top_speed_in_game':[], 'based_on':[], 'seats':[], 
    'weight_in_kg':[], 'drive_train':[], 'gears':[], 'release_date':[], 'release_dlc':[], 
    'top_speed_real':[], 'lap_time':[], 'bulletproof':[], 'weapon1_resistance':[], 
    'weapon2_resistance':[], 'weapon3_resistance':[], 'weapon4_resistance':[], 'weapon5_resistance':[], 'speed':[], 
    'acceleration':[], 'braking':[], 'handling':[], 'overall':[], 'vehicle_url':[]
})

t1 = time.time()
for link in batch:
    
    try:

        # ---- Setup ----
        driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
        url    = link
        driver.get(url)
        WDW(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="ja-current-content"]/div[1]/div[1]/h1')))

        # - Scroll to buttom
        scroll_to_bottom()

        # ---- Get HTML ----
        soup = BS(driver.page_source, 'lxml')      

        # ---- Get datapoints ----

        # -- General Info
        title             = try_except(func = soup.find('h1', class_ = 'contentheading').text.strip()) 
        vehicle_class     = try_except(func = extract_subtag_text_single(soup = soup, pattern = 'Vehicle Class'))
        manufacturer      = try_except(func = extract_subtag_text_single(soup = soup, pattern = 'Manufacturer'))
        features          = try_except(func = ', '.join(extract_subtag_text_multiple(soup = soup, pattern = 'Vehicle Features'))) 
        acquisition       = try_except(func = extract_subtag_text_single(soup = soup, pattern = 'Acquisition')) 
        price             = try_except(func = extract_subspan(soup = soup, pattern = 'GTA Online Price')) 
        storage_location  = try_except(func = extract_subtag_text_single(soup = soup, pattern = 'Storage Location')) 
        delivery_method   = try_except(func = extract_subtag_text_single(soup = soup, pattern = 'Delivery Method')) 
        modifications     = try_except(func = extract_subtag_text_single(soup = soup, pattern = 'Modifications')) 
        resale_flag       = try_except(func = extract_subtag_text_single(soup = soup, pattern = 'Sell')) 
        
        try:
            resale_price  = try_except(func = extract_subspan(soup = soup, pattern = 'Sell Price (Resale)').strip())
        except:
            resale_price  = 'NA'
            
        race_availability = try_except(func = extract_subtag_text_single(soup = soup, pattern = 'Race Availability'))
        top_speed_in_game = try_except(func = extract_subspan(soup = soup, pattern = 'Top Speed - Game Files').strip()) 
        based_on          = try_except(func = extract_subspan(soup = soup, pattern = 'Based on (Real Life)').strip()) 
        seats             = try_except(func = extract_subspan(soup = soup, pattern = 'Seats')) 
        weight_in_kg      = try_except(func = extract_subspan(soup = soup, pattern = 'Mass / Weight')) 
        
        try:
            drive_train   = try_except(func = extract_subspan(soup = soup, pattern = 'RWD')) 
        except:
            drive_train   = 'NA'
            
        try: 
            gears         = try_except(func = extract_subspan(soup = soup, pattern = 'Gears')) 
        except:
            gears         = 'NA'
            
        release_date      = try_except(func = extract_subspan(soup = soup, pattern = 'Release Date')) 
        release_dlc       = try_except(func = extract_subspan(soup = soup, pattern = 'DLC / Title Update')) 
        
        # -- Performance (Racing)
        top_speed_real    = try_except(func = extract_subspan(soup = soup, pattern = 'Top Speed - Real')) 
        lap_time          = try_except(func = extract_subspan(soup = soup, pattern = 'Lap Time')) 
        bulletproof       = try_except(func = extract_subspan(soup = soup, pattern = 'Bulletproof')) 

        # -- Weapon Resistance
        weapon1_resistance = try_except(func = extract_td_subtag(soup = soup, pattern = 'Homing Launcher / Oppressor Missiles / Jet Missiles'))
        weapon2_resistance = try_except(func = extract_td_subtag(soup = soup, pattern = 'RPG / Grenades / Sticky Bomb / MOC Cannon'))
        weapon3_resistance = try_except(func = extract_td_subtag(soup = soup, pattern = 'Explosive Rounds (Heavy Sniper Mk II)')) 
        weapon4_resistance = try_except(func = extract_td_subtag(soup = soup, pattern = 'Tank Cannon (Rhino / APC)')) 
        weapon5_resistance = try_except(func = extract_td_subtag(soup = soup, pattern = 'Anti-Aircraft Trailer Dual 20mm Flak')) 

        # -- Statistics
        speed               = try_except(func = soup.find('dd', class_ = 'field-entry speed').text.strip()) 
        acceleration        = try_except(func = soup.find('dd', class_ = 'field-entry acceleration').text.strip()) 
        braking             = try_except(func = soup.find('dd', class_ = 'field-entry braking').text.strip()) 
        handling            = try_except(func = soup.find('dd', class_ = 'field-entry handling').text.strip()) 
        overall             = try_except(func = soup.find('dd', class_ = 'field-entry overall').text.strip()) 
        
        # -- Link
        vehicle_url         = try_except(func = link)

        # ---- Append to dataframe ----
        df_gta = df_gta.append({    
            'title':              title, 
            'vehicle_class':      vehicle_class, 
            'manufacturer':       manufacturer, 
            'features':           features, 
            'acquisition':        acquisition, 
            'price':              price, 
            'storage_location':   storage_location,
            'delivery_method':    delivery_method, 
            'modifications':      modifications,
            'resale_flag':        resale_flag, 
            'resale_price':       resale_price, 
            'race_availability':  race_availability, 
            'top_speed_in_game':  top_speed_in_game, 
            'based_on':           based_on, 
            'seats':              seats, 
            'weight_in_kg':       weight_in_kg, 
            'drive_train':        drive_train, 
            'gears':              gears, 
            'release_date':       release_date, 
            'release_dlc':        release_dlc, 
            'top_speed_real':     top_speed_real, 
            'lap_time':           lap_time, 
            'bulletproof':        bulletproof, 
            'weapon1_resistance': weapon1_resistance, 
            'weapon2_resistance': weapon2_resistance, 
            'weapon3_resistance': weapon3_resistance, 
            'weapon4_resistance': weapon4_resistance, 
            'weapon5_resistance': weapon5_resistance, 
            'speed':              speed, 
            'acceleration':       acceleration, 
            'braking':            braking, 
            'handling':           handling, 
            'overall':            overall,
            'vehicle_url':        link
        }, ignore_index = True)
       
    except:
        pass
    
    driver.close()
    time.sleep(3)
    
t2 = time.time()

# ---- Check time to run ----
print("Scrape Time: ", t2 - t1) 

# ---- Inspect dataframe ----
df_gta.shape

# ---- Save to data folder
df_gta.to_csv(r'data/gtabase/gta_data_batch_3.csv')



# ---- SCRAPE UPGRADE COST ----
# - Code below is used to scrape the total cost to upgrade which was mistakenly omitted from the previous section

# ---- Batches ----
batch = links_list_final[0:401]
batch = links_list_final[401:709]

# ---- Dataframe placeholder ----
df_upgrade_cost = pd.DataFrame({'upgrade_cost':[], 'vehicle_url':[]})

# ---- For loop -----
# - Loops through each url and gets the `total cost to upgrade`
for link in batch:
    
    try:

        # ---- Setup ----
        driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
        url    = link
        driver.get(url)
        WDW(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="ja-current-content"]/div[1]/div[1]/h1')))

        # - Scroll to buttom
        scroll_to_bottom() # Run this function from previous section

        # ---- Get HTML ----
        soup = BS(driver.page_source, 'lxml')      

        # ---- Get datapoints ----
        try:
            upgrade_cost     = soup.find('div', class_ = 'field-entry garage-value').text        
        except:
            upgrade_cost     = 'NA'
            
        # -- Link
        vehicle_url         = link

        # ---- Append to dataframe ----
        df_upgrade_cost = df_upgrade_cost.append({
            'upgrade_cost': upgrade_cost,
            'vehicle_url':  link                                                 
          
        }, ignore_index = True)        
    except:
        pass
    
    driver.close()
    time.sleep(3)
    
# ---- Save to data folder ----
df_upgrade_cost.to_csv(r'data/gtabase/gta_data_upgrade_cost_2.csv')



