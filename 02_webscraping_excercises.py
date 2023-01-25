# WEBSCRAPING 101

# Requirements
import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml
import re

pd.options.display.max_columns = 30
pd.options.display.max_rows = 50
pd.options.display.expand_frame_repr = False

# URL
url = "https://techcrunch.com/category/apps/"

# Get HTML
page = requests.get(url)

# Get HTML as Text
soup = BeautifulSoup(page.text, "lxml")

# Tags
body_tags = soup.body


# EXCERCISE 01: TECH ARTICLE TOPICS
# - TECHCRUNCH

# Topics
topics = soup.find_all("a", {"class": "post-block__title__link"})
topic_list = []
topic = [i.text.strip() for i in topics]
topic_list.append(topic)


# Authors
authors = soup.find_all("span", {"class": "river-byline__authors"})
author_list = []
author = [i.text.strip() for i in authors]
author_list.append(author)

# Date
article_date = soup.find_all("time", {"class": "river-byline__time"})
date_list = []
date = [i["datetime"] for i in article_date]
date_list.append(date)

# Create Dataframe
tc_df = pd.DataFrame({"title":topic_list[0], "author":author_list[0], "date":date_list[0]})
tc_df.head()


# EXCERCISE 02: SCRAPE STOCK MARKET DATA POINTS
# - MARKETWATCH

# Get Page HTML
mwatch_url = "https://www.marketwatch.com/investing/stock/tsla?mod=search_symbol"
mwatch_page = requests.get(mwatch_url)
mwatch_soup = BeautifulSoup(mwatch_page.text, "lxml")

# Price
price = mwatch_soup.find("bg-quote", {"class": "value"}).text

# Close Price
close_price = mwatch_soup.find("td", class_ = "table__cell u-semi").text
close_price = float(close_price.strip("$"))

# Extract 52 Week Range
range_tag = mwatch_soup\
    .find_all("div", class_ = "column column--full supportive-data")[0]\
    .find_all("div")[6]\
    .find_all("span")[::2]

range_list = []
range_list.append([float(i.text) for i in range_tag])

# Extract Analyst Rating
rating = mwatch_soup.find_all("li", class_ = "analyst__option active")[0].text

# Create Dictionary
mwatch_dict = {
    "price"      :price, 
    "close_price":close_price, 
    "low"        :range_list[0][0], 
    "high"       :range_list[0][1], 
    "rating"     :rating
}


# EXCERCISE 03: SCRAPE NFL STATS
# - NFL.COM

nfl_url  = "https://www.nfl.com/standings/league/2021/REG"
nfl_page = requests.get(nfl_url)
nfl_soup = BeautifulSoup(nfl_page.text, "lxml")

# Get Table Tag HTML
nfl_table = nfl_soup.find("table", {"summary":"Standings - Detailed View"})

# Headers
nfl_headers_list = []
nfl_header = [i.text.strip() for i in nfl_table.find_all("th")]
nfl_headers_list.append(nfl_header)

df_nfl = pd.DataFrame(columns = nfl_headers_list[0])

# Rows
for i in nfl_table.find_all("tr")[1:]:
    first_td = i.find_all("td")[0].find("div", class_ = "d3-o-club-fullname").text.strip()
    data = i.find_all("td")[1:]
    row_data = [j.text.strip() for j in data]
    row_data.insert(0, first_td)
    length = len(df_nfl)
    df_nfl.loc[length] = row_data
    
df_nfl.head()


# EXCERCISE 04: SCRAPE MULTIPLE PAGES
# - CARPAGES.CA

carpages_url  = "https://www.carpages.ca/used-cars/search/?num_results=50&fueltype_id%5B0%5D=3&fueltype_id%5B1%5D=7&p=1"
carpages_page = requests.get(carpages_url)
carpages_soup = BeautifulSoup(carpages_page.text, "lxml")

# Create Dataframe Placeholder
df_carpages = pd.DataFrame({
    "link":[], 
    "title":[], 
    "detail":[], 
    "price":[], 
    "mileage":[], 
    "color":[], 
    "dealership":[], 
    "dealership_location":[]
})

# Initialize Counter
counter = 0

# While Loop
while counter < 10:
    
    # Get Car Postings
    postings = carpages_soup.find_all("div", class_ = "media soft push-none rule")
    for post in postings:       
        
        # Get Data Points
        link       = "https://www.carpages.ca" + post.find("a", class_ = "media__img media__img--thumb").get("href")
        title      = post.find("h4", class_ = "hN").text.strip()
        detail     = post.find("h5", class_ = "hN grey").text.strip()
        price      = post.find("strong", class_ = "delta").text.strip()
        
        miles_tag  = post.find("div", class_ = "grey l-column l-column--small-6 l-column--medium-4")
        miles = []
        for span in miles_tag:
            miles.append(span.get_text().strip())
        miles = "".join(miles)
        
        color  = post.find_all("div", class_ = "grey l-column l-column--small-6 l-column--medium-4")[1].text.strip()
        if len(color) == 0:
            color = "NA"
        else:
            color = color
        
        dealer     = post.find("hgroup", class_ = "vehicle__card--dealerInfo").find("h5", class_ = "hN").text
        dealer_loc = post.find("hgroup", class_ = "vehicle__card--dealerInfo").find("p", class_ = "hN").text   
        
        # Create Dataframe
        df_carpages = df_carpages.append({
            "link":link, 
            "title":title, 
            "detail":detail, 
            "price":price, 
            "mileage":miles, 
            "color":color, 
            "dealership":dealer, 
            "dealership_location":dealer_loc
        }, ignore_index = True) 
            
    # Next Page URL
    next_page = carpages_soup.find("a", class_ = "nextprev").get("href")
    next_page_full = "https://www.carpages.ca" + next_page

    # Next Page HTML
    carpages_url = next_page_full
    carpages_page = requests.get(carpages_url)
    carpages_soup = BeautifulSoup(carpages_page.text, "lxml")
    
    counter += 1
    
df_carpages
df_carpages.info()
