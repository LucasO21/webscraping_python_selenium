# SELENIUM TUTORIAL

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
    
    break
   
# Wait Times

# - Open Webpage
driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
driver.get("https://www.google.com/")

# - Enter Search Criteria & Enter
box = driver.find_element("xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
box.send_keys("arsenal fc")
box.send_keys(Keys.ENTER)

# - Wait 10 Seconds
element = WDW(driver, 10).until(EC.presence_of_element_located((By.ID, 'tophf')))
#time.sleep(5)

# - Click Image Button
driver.find_element('xpath', '//*[@id="hdtb-msb"]/div[1]/div/div[3]/a').click()



# SELENIUM EXCERCISE

# - Initialize Webdriver & Go to Google.Com
driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
driver.get("https://www.google.com/")

# Inputs Into Google Search Box & Hit Enter
box = driver.find_element("xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
box.send_keys("top 100 movies of all time")

# - Press Enter Button to Search
box.send_keys(Keys.ENTER)

# - Wait 3 Seconds
time.sleep(3)

# - Click The Link for IMDB
driver.find_element('xpath', '//*[@id="rso"]/div[1]/div/div/div[1]/div/a/h3').click()

# - Wait 3 Seconds
time.sleep(3)

# - Scroll Until Jaws 
driver.execute_script('window.scrollTo(0,22500)')

# - Take Screenshot
driver.save_screenshot("png/imdb.png")


#######################################################################################################################

# INFINITE SCROLLING (NIKE WEBSIE)

# - Setup
driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
driver.get("https://www.nike.com/w/sale-3yaep/")
time.sleep(10)

# - Grab The Height of The Page
last_height = driver.execute_script('return document.body.scrollHeight')

# - Scroll To The Bottom of The Page
t1 = time.time()
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height
t2 = time.time()

#  - Grab HTML
soup = BS(driver.page_source, 'lxml')

# - Grab Product Cards
product_card = soup.find_all('div', class_ = 'product-card__body')

# - Create Dataframe Placeholder
df_nike = pd.DataFrame({'link':[], 'title':[], 'desc':[], 'price':[], 'sale_price':[]})

# - Grab Data Points
t3 = time.time()
for product in product_card:
    
    try:
        link       = product.find('a', class_ = 'product-card__img-link-overlay').get('href')
        title      = product.find('div', class_ = 'product-card__title').text
        desc       = product.find('div', class_ = 'product-card__subtitle').text
        #color      = product.find('div', class_ = 'product-card__product-count font-override__body1').text
        sale_price = product.find('div', class_ = 'product-price is--current-price css-1ydfahe').text
        price      = product.find('div', class_ = 'product-price us__styling is--striked-out css-0').text
        
        df_nike =  df_nike.append({
        "link":link,
        "title":title,
        "desc":desc,
        "price":price,
        "sale_price":sale_price
        }, ignore_index = True)
        
    except:
        pass
    
t4 = time.time()

df_nike.to_csv('data/webscraping_nike.csv')

print("Scroll Time: ", t2 - t1)
print("Scrape Time: ", t4 - t3)




