import json
from threading import Thread
from selenium.webdriver.common.by import By

import requests 
from bs4 import BeautifulSoup
import concurrent.futures


links = []
for i in range(1, 50):
    url = f"https://www.yphs.tp.edu.tw/category/news/news1/page/{i}/"
    res = requests.get(url) 
    Soup = BeautifulSoup(res.text, 'html.parser')
    
    for i in Soup.find_all(class_ = "nt_subject"):
        links.append(i.find(class_='news_title')["href"])
print(links)
db = {}

def scrape(link):
    res = requests.get(link) 
    Soup = BeautifulSoup(res.text, 'html.parser')

    # print(Soup.find(class_ = "newstd").text)

    nd = {  "title":Soup.find(class_ = "newstd").text,
            "content":Soup.find(class_ = "content").text,
            "time":Soup.select(".news_date .newstd")[0].text
        }
    if nd["time"] not in db:
        db[nd["time"]] = []
    db[nd["time"]].append(nd)
    # print(len(db[nd["time"]]))
    # print(nd["time"])

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scrape, links)


for i in links:
    scrape(i)
with open("data_RCC.json", 'w') as f:
    json.dump(db, f, indent=4)
