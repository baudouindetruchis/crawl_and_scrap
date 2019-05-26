import datetime
import logging
import pandas as pd

import requests
from bs4 import BeautifulSoup


logging.basicConfig(filename='scrap.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
    }


# grab all links
anchors = page_soup.find_all('a')
links = []
for anchor in anchors:
    links.append(anchor.get('href'))
links_count = len(links)
logging.info('found {} links'.format(links_count))
