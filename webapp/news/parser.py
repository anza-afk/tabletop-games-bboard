from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re

url = 'https://www.bgeek.ru/category/%d0%bd%d0%b0%d1%81%d1%82%d0%be%d0%bb%d1%8c%d0%bd%d1%8b%d0%b5-%d0%b8%d0%b3%d1%80%d1%8b/'
my_session = requests.Session()


def get_html(url:str, session:requests.Session) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    try:
        result = session.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return None


def get_game_links(html: str) -> list:
    try:
        soup = BeautifulSoup(html, 'html.parser')
        news_list = soup.find('div', class_='article-container').findAll('article')
        result_news = []
        for news in news_list:
            news_link = news.find('div', class_='entry-content').find('a')['href']
            result_news.append(news_link)
    except FileNotFoundError:
        result_news = []
    return result_news


def get_one_news(html: str) -> dict:
    news_data = {
        'title' : None,
        'author' : None,
        'published' : None,
        'content' : None,
        'image': None
    }
    try:
        soup = BeautifulSoup(html, 'html.parser')
        title_data = soup.find('div', class_="article-content clearfix")
        news_data['title'] = re.sub("[\n\r\t]", '', title_data.find('header', class_="entry-header").find('h1').text)
        news_data['author'] = re.sub("[\n\r\t]", '', title_data.find('a', class_="url fn n").text)
        news_data['published'] = title_data.find('time', class_="entry-date published")['datetime'].replace('T', ' ')
        news_data['content'] = title_data.find('div', class_="entry-content clearfix").text.replace('\nПохожее\n','')
        news_data['image'] = soup.find('div', class_="featured-image").find('img')['src']
        try:
            news_data['published'] = datetime.strptime(news_data['published'], '%Y-%m-%d %H:%M:%S%z')
        except(ValueError):
            news_data['published'] = datetime.now()
    except FileNotFoundError:
        news_data = []
    return news_data


result_news = [get_one_news(get_html(link, my_session)) for link in get_game_links(get_html(url, my_session))]
