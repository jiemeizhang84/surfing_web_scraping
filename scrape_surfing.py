import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import pymongo

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.surf_db

# Drops collection if available to remove duplicates
db.surf_summary.drop()

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

surf_dict = {}
i = 1

url = "https://www.surfline.com/surf-reports-forecasts-cams/costa-rica/3624060"
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, "html.parser")

results = soup.find_all("a", class_="sl-cam-list-link")

for result in results:
    surf_dict["_id"] = i
    surf_dict["location_name"] = result.find("h3", class_="sl-spot-details__name").get_text()
    surf_dict["wave_height"] = result.find("span", class_="quiver-surf-height").get_text()
    weather_url = "https://www.surfline.com"+result['href']
    surf_dict["url"] = weather_url

    browser.visit(weather_url)
    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, "html.parser")

    surf_dict["water_temp"] = weather_soup.find("div", class_="sl-wetsuit-recommender__weather").find_all("div")[0].text
    surf_dict["air_temp"] = weather_soup.find("div", class_="sl-wetsuit-recommender__weather").find_all("div")[1].text

    db.surf_summary.insert_one(surf_dict)
    i = i + 1

    
