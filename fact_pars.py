from bs4 import BeautifulSoup as bs
import requests


URL = 'https://www.factroom.ru/random/facts?list='


def parse():
    r = requests.get(URL)
    text = r.text
    soup = bs(text, "html.parser")
    i = soup.find_all('img')[2]

    return (i.get('alt'), i.get('src'))
