import json
from selenium import webdriver
from selenium.webdriver.common.by import By

from tqdm import tqdm

import requests 
from bs4 import BeautifulSoup


links = []
for i in range(1, 50):
    url = f"https://www.yphs.tp.edu.tw/category/news/news1/page/{i}/"
    res = requests.get(url) 
    Soup = BeautifulSoup(res.text, 'html.parser')
    
    for i in Soup.find_all(class_ = "nt_subject"):
        links.append(i.find(class_='news_title')["href"])
# print(links)

db = {}
for link in tqdm(links):
    res = requests.get(link) 
    Soup = BeautifulSoup(res.text, 'html.parser')

    # print(Soup.find(class_ = "newstd").text)

    nd = {  "title":Soup.find(class_ = "newstd").text,
            "content":Soup.find(class_ = "content").text,
            "time":Soup.select(".news_date .newstd")[0].text,
            "category":[i.text for i in Soup.select(".news_cat .newstd")],
            "unit":Soup.select(".news_unit .newstd")[0].text,
            "type":Soup.select(".news_type .newstd")[0].text,
            "view":int(Soup.select(".news_view .newstd")[0].text.strip().replace(',', '')),
            "Attached":Soup.select(".newsth .news_attach\ newstd")
        }
    if nd["time"] not in db:
        db[nd["time"]] = []
    db[nd["time"]].append(nd)
    # print(len(db[nd["time"]]))
    # print(nd["time"])

with open("data.json", 'w', encoding="utf8") as f:
    json.dump(db, f, indent=4, ensure_ascii=False)
