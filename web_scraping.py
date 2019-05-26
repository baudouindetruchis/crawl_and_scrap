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

urls = ['https://www.bbc.com/news/business-38507481'
#        , 'https://www.bbc.com/news/business/companies'
#        , 'https://www.bbc.com/news/business/economy'
#        , 'https://www.bbc.com/news/business'
        ]

logging.info('START')

# test connection
response = requests.get(url, headers=headers, timeout=5)
if response.status_code != 200:
    logging.warning(response)

page_soup = BeautifulSoup(response.text, 'lxml')

nav_bar = page_soup.find('ul', {'class':'gs-o-list-ui--top-no-border nw-c-nav__wide-sections'}).findAll('a')

cats = []
pages = []

for url in urls:
    cats.append(cat.get('href'))
    
for cat in cats:
    url = main_url + cat
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code != 200:
        logging.warning(response)
        
    page_soup = BeautifulSoup(response.text, 'lxml')
    try:
        sub_nav = page_soup.find('ul', {'class':'gs-o-list-ui--top-no-border nw-c-nav__secondary-sections'}).findAll('a')
    except:
        try:
            sub_nav = page_soup.find('ul', {'class':'js-navigation-panel-secondary'}).findAll('a')
        except:
            pass
    for page in sub_nav:
        pages.append(main_url + page.get('href'))
    print(1)
    


#grab every article in 'latest updates'
containers = page_soup.find_all('article', {'class':'lx-stream-post gs-u-align-left lx-stream-post--has-meta'})

articles = pd.DataFrame(columns=['date','title','summary'])

for container in containers:
    # get creation date - if no => take current one at UTC
    try:
        article_date = container.div.time.find('span', {'class':'qa-meta-date gs-u-mr gs-u-display-inline-block'}).text
    except:
        article_date = datetime.datetime.utcnow().strftime('%d %B')

    # get creation time
    try:
        article_time = container.div.findAll('span')[4].text
    except:
        article_time = ''

    # parse into datetime
    article_datetime = datetime.datetime.strptime(
            datetime.datetime.utcnow().strftime('%Y')
            + article_date + article_time, '%Y%d %B%H:%M')

    # grab article title
    try:
        article_title = container.find('span', {'class':'lx-stream-post__header-text'}).text
    except:
        article_title = ''

    # grab article summary
    try:
        article_summary = container.findAll('p')[-1].text
    except:
        try:
            article_summary = container.find('pre').text
        except:
            article_summary = ''

    articles = articles.append({'date':article_datetime,
                                'title':article_title,
                                'summary':article_summary}, ignore_index=True)

print(articles)

logging.info('FINISHED')

