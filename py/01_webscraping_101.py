# WEBSCRAPING 101

# Requirements
import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml
import re
import time


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


# SCRAPING MULTIPLE PAGES (AIRBNB)

# Setup
airbnb_url  = "https://www.airbnb.com/s/Reykjavik--Iceland/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Reykjavik%2C%20Iceland&place_id=ChIJw-3c7rl01kgRcWDSMKIskew&date_picker_type=calendar&checkin=2023-05-31&checkout=2023-06-05&source=structured_search_input_header&search_type=autocomplete_click"
airbnb_page = requests.get(airbnb_url)
airbnb_soup = BeautifulSoup(airbnb_page.text, "lxml")

# Create Dataframe Placeholder
df_airbnb = pd.DataFrame({"title":[], "description":[], "beds":[], "price":[], "rating":[]})

# Loop Through Pages 
while True:
    
    # Get Postings
    postings = airbnb_soup.find_all("div", class_ = "c4mnd7m dir dir-ltr")
    for post in postings:
        
        # Get Data
        try:
            title  = post.find("div", class_ = "t1jojoys dir dir-ltr").text
            desc   = post.find("span", class_ = "t6mzqp7 dir dir-ltr").text
            rating = post.find("span", class_ = "r1dxllyb dir dir-ltr").text
            beds   = post.find("span", class_ = "dir dir-ltr").text
            
            price_str = post.find("div", class_ = "p11pu8yw dir dir-ltr").text
            start     = price_str.find("night") + len("night")
            end       = price_str.find("per")
            price     = price_str[start:end].strip()
            
            # Create Dataframe
            df_airbnb = df_airbnb.append({"title":title, "description":desc, "beds":beds, "price":price, "rating":rating}, ignore_index = True)
        
        except:
            pass        
    
    # Next Page Formate
    next_page = airbnb_soup.find("a", {"aria-label":"Next"}).get("href")
    next_page_full = "https://www.airbnb.com" + next_page
    
    # Next Page HTML
    airbnb_url = next_page_full
    airbnb_page = requests.get(airbnb_url)
    airbnb_soup = BeautifulSoup(airbnb_page.text, "lxml")
    
    break   


# Format Dataframe
df_airbnb = df_airbnb\
    .assign(rating = lambda x: x["rating"].replace("New", "0.00 (0)"))\
    .assign(rating_score = lambda x: x["rating"].str.split(" ").str[0].astype(float))\
    .assign(rating_count = lambda x: x["rating"].str.split(" ").str[1].str.extract("(\d+)").astype(int))\
    .drop("rating", axis = 1)
    

    







