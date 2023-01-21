# WEBSCRAPING 101

# Requirements
import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml
import re


# SCRAPING TABLES

# Setup
url  = "https://www.worldometers.info/world-population/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")

# Get Table Tag HTML
table = soup.find("table", class_ = "table table-striped table-bordered table-hover table-condensed table-list")

# Get Column Headers
headers_list = []
header = [i.text for i in table.find_all("th")]
headers_list.append(header)

df = pd.DataFrame(columns = headers_list)

# Get Rows
for i in table.find_all("tr")[1:]:
    row_data = i.find_all("td")
    row = [j.text for j in row_data]
    length = len(df)
    df.loc[length] = row


# SCRAPING AIRBNB
#  - Sraping Multiple Pages

# 1 Example
airbnb_url  = "https://www.airbnb.com/s/Honolulu/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&date_picker_type=calendar&checkin=2023-03-08&checkout=2023-03-13&source=structured_search_input_header&search_type=user_map_move&query=Honolulu%2C%20Oahu%2C%20Hawaii%2C%20United%20States&place_id=ChIJTUbDjDsYAHwRbJen81_1KEs&ne_lat=21.352946159824135&ne_lng=-157.76304531451535&sw_lat=21.231068788705716&sw_lng=-157.88234997149777&zoom=13&search_by_map=true"
airbnb_page = requests.get(airbnb_url)
airbnb_soup = BeautifulSoup(airbnb_page.text, "lxml")

# Function
def get_data_list(html_tag, html_tag_class):
    
    list     = []
    div_all  = airbnb_soup.find_all(html_tag, class_ = html_tag_class)
    data     = [i.text.strip() for i in div_all]
    list.append(data)
    
    return list
    
# Title 
title_list = get_data_list(html_tag = "div", html_tag_class = "t1jojoys dir dir-ltr")

# Description
desc_list = get_data_list(html_tag = "span", html_tag_class = "t6mzqp7 dir dir-ltr")

# Beds 
bed_list = get_data_list(html_tag = "span", html_tag_class = "dir dir-ltr")

# Price
price_list = get_data_list(html_tag="div", html_tag_class="p11pu8yw dir dir-ltr")

# Rating
rating_list = get_data_list(html_tag="span", html_tag_class="t5eq1io r4a59j5 dir dir-ltr")

# Dataframe
df_airbnb = pd.DataFrame({
    "title":title_list[0],
    "description":desc_list[0],
    "bedrooms":bed_list[0],
    "price":price_list[0],
    "rating":rating_list[0]
})\
    .assign(rating = lambda x: x["rating"].replace("New", "0.00 (0)"))\
    .assign(rating_score = lambda x: x["rating"].str.split(" ").str[0].astype(float))\
    .assign(rating_count = lambda x: x["rating"].str.split(" ").str[1].str.extract("(\d+)").astype(int))\
    .drop("rating", axis = 1)\
    .assign(price_per_night = lambda x: x["price"].str.split(" ").str[0])\
    .drop("price", axis = 1)\
    .assign(price_per_night = lambda x: x["price_per_night"].str.split("$").str[-1].astype(float))
    
df_airbnb.info()
    

# Scale To Multiple Pages
while True:
    
    url_page_list = []    
    url_base = "https://www.airbnb.com"
    next_page_url = airbnb_soup.find("a", {"aria-label":"Next"}).get("href")
    next_page_url_full = url_base + next_page_url
    url_page_list.append(next_page_url_full)





