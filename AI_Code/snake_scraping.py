# Importing Libraries

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import time
import requests,json, re
import bs4
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager
import time

from tqdm import tqdm
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

val = "http://snakedb.org/"
time.sleep(5)
wait = WebDriverWait(driver, 10)

driver.get(val)


get_url = driver.current_url
wait.until(EC.url_to_be(val))


if get_url == val:
    page_source = driver.page_source
time.sleep(10)
button1 = driver.find_element("xpath","/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[1]/label")
button1.click()
button2 = driver.find_element("xpath","/html/body/main/div[2]/div[2]/div/div[1]/div[2]/div[1]/label")
button2.click()
button3 = driver.find_element("xpath","/html/body/main/div[2]/div[2]/div/div[1]/div[3]/div[1]/label")
button3.click()
button4 = driver.find_element("xpath","/html/body/main/div[2]/div[2]/div/div[1]/div[5]/div[2]/div[2]/div/div/label")
button4.click()
button5 = driver.find_element("xpath",'//*[@id="search-button"]')
button5.click()
time.sleep(10)
lval1 = []
lval2 = []
lval3 = []
lval4 = []
for i in tqdm(range(1,3665)):
    try:
        val1 = driver.find_element("xpath",f'//*[@id="searchResult"]/div[{i}]/a/h2')
        val2 = driver.find_element("xpath",f'//*[@id="searchResult"]/div[{i}]/a/p[1]')
        val3 = driver.find_element("xpath",f'//*[@id="searchResult"]/div[{i}]/a/p[2]')  
        val4 = driver.find_element("xpath",f'//*[@id="searchResult"]/div[{i}]/a/p[3]')  
        if val1.text == '' or val2.text == '' or val3.text == '' or val4.text == '':
            print("skip")
        else:
            lval1.append(val1.text)
            lval2.append(val2.text)
            lval3.append(val3.text)
            lval4.append(val4.text)
    except Exception as e:
        print("E",e)

df = pd.DataFrame({
    'snake_name': lval1,
    'scientific_name': lval2,
    'toxicity': lval3,
    'size': lval4
})

# print(df)

# Save the DataFrame to a CSV file
csv_file_path = 'snakes_data.csv'  # Specify the path and file name here
df.to_csv(csv_file_path, index=False)  # Set index=False to exclude row indices from the CSV

print(f"Data saved to '{csv_file_path}'")

