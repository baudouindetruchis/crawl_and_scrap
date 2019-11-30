import datetime
import logging
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import random
import os


# Create log if none 
if not os.path.isfile('scrap.log'):
    file = open("scrap.log","w+")
    file.close()
        
logging.basicConfig(filename='scrap.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

user_agent_list = pd.read_csv('user_agents.csv').chrome_user_agent.to_list()

headers = {
        "User-Agent":random.choice(user_agent_list),
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT":"1",
        "Connection":"close",
        "Upgrade-Insecure-Requests":"1"
    }

# Product url = server_url + product asin
server_url = 'https://www.amazon.com/dp/'

# Asin to scrap
asins_list = pd.read_csv('asins.csv').asin.to_list()

logging.info('START')


for asin in asins_list:
    url = server_url + asin
    
    # Test connection + save response
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code != 200:
        logging.warning(response)
        continue
    
    # lxml : fast parser
    page_soup = BeautifulSoup(response.text, 'lxml')
    
    # Get price
    try:
        price = page_soup.find('span', {'id':'priceblock_ourprice'}).text.replace(',','')
    except:
        try:
            price = page_soup.find('span', {'id':'priceblock_pospromoprice'}).text.replace(',','')
        except:
            try:
                price = page_soup.find('span', {'id':'priceblock_dealprice'}).text.replace(',','')
            except:
                price = np.nan
    
    # Get shipment price
    try:
        shipment_price = page_soup.find('span', {'id':'ourprice_shippingmessage'}).find('span', {'class':'a-size-base a-color-secondary'}).text.split()[1]
    except:
        try:
            shipment_price = page_soup.find('span', {'id':'dealprice_shippingmessage'}).find('span', {'class':'a-size-base a-color-secondary'}).text.split()[1]
        except:
            shipment_price = np.nan
        
    # Get rating
    try:
        rating = page_soup.find('div', {'id':'averageCustomerReviews_feature_div'}).find('span', {'class':'a-icon-alt'}).text.split()[0]
    except:
        rating = np.nan
    
    # Get ratings count
    try:
        ratings_count = page_soup.find('div', {'id':'averageCustomerReviews_feature_div'}).find('span', {'id':'acrCustomerReviewText'}).text.split()[0].replace(',','')
    except:
        ratings_count = np.nan

    # Get scrap date 
    scrap_date = datetime.datetime.utcnow().strftime('%y/%m/%d')
    
    # Saving to csv
    with open('amazon_scraping.csv', 'a') as file:
        file.write(scrap_date + ',' + asin + ',' + str(price) + ',' + str(shipment_price) + ',' \
                   + str(rating) + ',' + str(ratings_count) + '\n') 
    
    # Random time sleep between queries
    time.sleep(random.randint(0,3))

logging.info('FINISHED')