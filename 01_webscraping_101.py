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


