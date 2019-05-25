import os
import time
import requests

from bs4 import BeautifulSoup
import urllib.request

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
    }

url = 'https://www.amazon.fr/s?k=google+pixel&__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_2'

response = requests.get(url, headers=headers, timeout=5)

if response.status_code != 200:
    print(response)
#    return False

soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')
containers = soup.find_all('div', {'class':'sg-row'})
