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
        , 'https://www.bbc.com/news/business/companies'
        , 'https://www.bbc.com/news/business/economy'
        , 'https://www.bbc.com/news/business'
        ]

logging.info('START')

df = pd.DataFrame(columns=['date','title','summary','link'])

for url in urls:

    # test connection
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code != 200:
        logging.warning(response)

    page_soup = BeautifulSoup(response.text, 'lxml')

    df = pd.concat((df,get_articles(page_soup)), axis=0)

logging.info('FINISHED')


def get_articles(page_soup):
    """
    grab every article in 'latest updates'
    """
    containers = page_soup.find_all('article', {'class':'lx-stream-post gs-u-align-left lx-stream-post--has-meta'})

    articles = pd.DataFrame(columns=['date','title','summary','link'])

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

        # grab article link
        try:
            article_link = container.find('a').get('href')
        except:
            article_link = ''

        #save article info in a dataframe
        articles = articles.append({'date':article_datetime,
                                'title':article_title,
                                'summary':article_summary,
                                'link':article_link}, ignore_index=True)
    return articles
