# MIXCLOUD BOT

# Imports
import pandas as pd
import numpy as np
import random
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

# Random Number
n = random.randint(1, 3)
num_repeats = n

for i in range(num_repeats):

    # Got To Website
    driver = webdriver.Chrome("../../chrome_driver/chromedriver_mac64/chromedriver")
    driver.get("https://m.mixcloud.com/DJChuky/rva-zouk-movement-anniversary-weekender-friday-pm/")
    element = WDW(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/section/div[2]/div/div/div[2]/div/div[1]/section/div[1]/div[1]/div[1]/div[1]/span/span[1]')))

    # Click Play
    play = driver.find_element('xpath', '//*[@id="react-root"]/div/section/div[2]/div/div/div[2]/div/div[1]/section/div[1]/div[1]/div[1]/div[1]/span/span[1]') 
    play.click()

    # Wait for 10 seconds
    time.sleep(40)

    # Close Webpage
    driver.quit()
    
    # Print N
    print(n)

