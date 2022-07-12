from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests

import certifi
ca = certifi.where()


client = MongoClient('mongodb+srv://test:sparta@cluster0.ysqxz.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

driver = webdriver.Chrome('./chromedriver')

url = "http://ticket.interpark.com/TPGoodsList.asp?Ca=Eve&SubCa=Eve_C&Sort=2"

driver.get(url)
time.sleep(5)

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

places = soup.select("body > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > div.con > div > table > tbody > tr")

for place in places:
    title = place.select_one("td.RKtxt > span > a").text
    image = place.select_one("td.RKthumb > a > img")['src']
    start_date = place.select_one("td:nth-child(4)").text[0:12]
    end_date = place.select_one("td:nth-child(4)").text[-11:]
    all_date = (start_date+end_date).strip()
    url = place.select_one("td.RKthumb > a")['href']
    where_place = place.select_one("td:nth-child(3) > a").text
    print(title, image, all_date, url, where_place)
    doc = {
        "title": title,
        "image": image,
        "all_date": all_date,
        "url": url,
        "where_place":where_place
        }
    db.festivals.insert_one(doc)
