# grab all links
anchors = page_soup.find_all('a')
links = []
for anchor in anchors:
    links.append(anchor.get('href'))
links_count = len(links)
logging.info('found {} links'.format(links_count))
