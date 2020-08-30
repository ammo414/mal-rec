from bs4 import BeautifulSoup as bs
import requests


def pulltitlescore(aid):
    url = f'https://myanimelist.net/anime/{aid}'
    page = requests.get(url)
    soup = bs(page.content, features='html.parser')
    results = soup.find(class_='title-name')
    title = str(results)[23:][:-5]

    results = soup.find(itemprop='ratingValue')
    rating = float(str(results).split('ratingValue')[1][2:6])

    return {'title':title, 'score':rating}