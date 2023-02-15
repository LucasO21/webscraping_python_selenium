# PYTHON SCRIPT FOR CLEANING GTA VEHICLE DATA

# IMPORTS 
import pandas as pd
import os
import re

# OPTIONS
pd.set_option('display.max_columns', None)

# GET WORKING DIRECTORY
os.chdir(os.getcwd())

# LOAD DATA

# - Vehicle Data
csv1 = pd.read_csv("data/gtabase/gta_data_batch_1.csv")
csv2 = pd.read_csv("data/gtabase/gta_data_batch_2.csv")
csv3 = pd.read_csv("data/gtabase/gta_data_batch_3.csv")

df_vehicle_details = pd.concat([csv1, csv2, csv3])\
    .drop_duplicates()\
    .drop("Unnamed: 0", axis=1)

# - Upgrade Cost Data
upgrade_cost_1 = pd.read_csv("data/gtabase/gta_data_upgrade_cost_1.csv")
upgrade_cost_2 = pd.read_csv("data/gtabase/gta_data_upgrade_cost_2.csv")

df_upgrade_cost = pd.concat([upgrade_cost_1, upgrade_cost_2])\
    .drop_duplicates()\
    .drop("Unnamed: 0", axis=1)
    
# - Join Vehicle Details and Upgrade Cost
df_uncleaned = pd.merge(df_vehicle_details, df_upgrade_cost, how="left", left_on="vehicle_url", right_on="vehicle_url")


# DATA CLEANING

# - Convert NAN to NA
df_clean = df_uncleaned.replace(float("nan"), "NA")

# - Remove NA Rows
df_clean = df_clean[df_clean["manufacturer"].notna()]

# - Clean title column
df_clean['title'] = df_clean['title'].apply(lambda x: x.replace('GTA 5:', '').strip())
df_clean['title']

# - Clean acquisition column
df_clean['acquisition'] = df_clean['acquisition'].apply(lambda x: x.replace('/ found', '').strip())
df_clean['acquisition']

# - Clean price column
df_clean['price'] = df_clean['price'].apply(lambda x: re.sub(r'\D', '', x)).astype('int')
df_clean['price']

# - Clean resale column
df_clean[['resale_price_normal', 'resale_price_upgraded']] = df_clean['resale_price'].str.split('\\(', expand = True)

df_clean['resale_price_normal'] = df_clean['resale_price_normal'].str.replace('\D', '').str.strip()

df_clean['resale_price_upgraded'] = df_clean['resale_price_upgraded'].str.replace('\D', '').str.strip()

df_clean['resale_price_normal']
df_clean['resale_price_upgraded']

# - Clean resale flag
df_clean['resale_flag'] = np.where(df_clean['resale_flag'].str.contains('Can be sold'), 'Yes', 'No')
df_clean['resale_flag']

# - Upgrade Cost
df_clean['upgrade_cost'] = df_clean['upgrade_cost'].str.replace('\D', '').str.strip()
df_clean['upgrade_cost']

# - Top speed
df_clean['top_speed_in_game'] = df_clean['top_speed_in_game'].str.replace(r'\s*\([^()]*\)', '', regex=True).str.replace('mph', '').str.strip().astype('float')
df_clean['top_speed_in_game']

# - Release date
df_clean['release_date'] = pd.to_datetime(df_clean['release_date'], format = '%B %d, %Y')
df_clean['release_date']

# - Weight
df_clean['weight_in_kg'] = df_clean['weight_in_kg'].str.replace('\D', '').str.strip().astype('int')
df_clean['weight_in_kg']

# - Top speed
df_clean['top_speed_real'] = df_clean['top_speed_real'].str.replace(r'\s*\([^()]*\)', '', regex=True).str.replace('mph', '').str.strip().astype('float')
df_clean['top_speed_real']

# - Lap time
minutes, seconds_milliseconds = df_clean['lap_time'].str.split(':', 1).str
seconds, milliseconds = seconds_milliseconds.str.split('.').str
minutes = minutes.astype(float)
seconds = seconds.astype(float)
milliseconds = milliseconds.astype(float)
df_clean['lap_time'] = minutes * 60 + seconds + milliseconds / 1000

df_clean['lap_time']

# - Statistics columns
df_clean['speed'] = df_clean['speed'].str.replace('Speed', '').str.strip().astype('float')
df_clean['acceleration'] = df_clean['acceleration'].str.replace('Acceleration', '').str.strip().astype('float')
df_clean['braking'] = df_clean['braking'].str.replace('Braking', '').str.strip().astype('float')
df_clean['handling'] = df_clean['handling'].str.replace('Handling', '').str.strip().astype('float')
df_clean['overall'] = df_clean['overall'].str.replace('Overall', '').str.strip().astype('float')

df_clean.info()

# SAVE CLEAN DATA
df_clean.to_csv('data/gtabase/gta_data_cleaned.csv')

