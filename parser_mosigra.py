from cgitb import html
import requests
from bs4 import BeautifulSoup as bs
import re


def get_html(url):
    try: 
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False


def get_last_page(html):
    soup = bs(html, 'html.parser')
    url = soup.find('a', class_='last')
    return int(re.split(r"=|&",str(url))[3])


def get_urls(html):  
    links = []  
    soup = bs(html, 'html.parser')
    games = soup.find('div', class_='products-container').findAll('article')
    for game in games:
        links.append(game.find('a')['href'])
    return links


if __name__ == '__main__':
    url = 'https://www.mosigra.ru/nastolnye-igry/?page='
    for page in range(1, (get_last_page(get_html(url))+1)):
        current_page = get_html(f'{url}{page}')
        with open('links_list.txt', 'a') as f:
            for link in get_urls(current_page):
                f.write(link+'\n')
 