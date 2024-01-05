from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from pymongo import MongoClient
import certifi
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

password = 'alifah82'
cxn_str = f'mongodb+srv://Alifah:{password}@cluster0.ahwwxzc.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(cxn_str)
db = client.dbsparta_plus_week2

chrome_options = Options()
chrome_service = Service('./chromedriver.exe') 
driver = webdriver.Chrome(service=chrome_service)

url = "https://www.yelp.com/search?cflt=restaurants&find_loc=San+Francisco%2C+CA"

driver.get(url)
sleep(5)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
sleep(5)


access_token = 'pk.eyJ1IjoibWlmdGFjaHVsaHVkYWFhIiwiYSI6ImNsOHZoMmVseDBkc2EzdmxtZmxmdzk5YXgifQ.q60T1roWKtzhwf1GJcYvSw'
long = -122.420679
lat = 37.772537

# keeps track of first search result number
start = 0

for _ in range(5):
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    restaurants = soup.select('div[class*="arrange-unit__"]')
    for restaurant in restaurants:
        business_name = restaurant.select_one('div[class*="businessName__"]')
        if not business_name:
            continue
        name = business_name.text.split('.')[-1].strip()
        categories_price_location = restaurant.select_one('div[class*="priceCategory__"]')
        spans = categories_price_location.select('span')
        categories = spans[0].text
        location = spans[1].text
        geo_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?proximity={long},{lat}&access_token={access_token}"
        geo_response = requests.get(geo_url)
        geo_json = geo_response.json()
        center = geo_json['features'][0]['center']
        print(name, categories, location, center)
        # pencarian untuk mensimulasikan pergerakan laman
        doc = {
            'name': name,
            'categories': categories,
            'location': location,
            'coordinates': center,
        }
        db.resto.insert_one(doc)
    start += 10
    driver.get(f'{url}&start={start}')
    sleep(5)
     
    


driver.quit()