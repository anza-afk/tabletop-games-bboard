from bs4 import BeautifulSoup
# import os
import requests


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


my_session = requests.Session()
# html_news = os.path.join(os.path.dirname(__file__), "news_game.html")
html_news = get_html(
    "https://www.bgeek.ru/category/%d0%bd%d0%b0%d1%81%d1%82%d0%be%d0%bb%d1%8c%d0%bd%d1%8b%d0%b5-%d0%b8%d0%b3%d1%80%d1%8b/%d0%bd%d0%be%d0%b2%d0%be%d1%81%d1%82%d0%b8/",
    my_session
)


def get_game_news(html: str) -> list[dict]:
    try:
        # with open(html_news, "r", encoding="utf8") as f:
        #     html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        news_list = soup.find('div', class_='article-container').findAll('article')
        result_news = []
        for news in news_list:
            title_news = news.find('h2').text.replace('\n', '')
            date_news = news.find('time')['datetime']
            text_news = news.find('div', class_='entry-content').find('p').text
            img_news = news.find('img')['src']
            href_news = news.find('div', class_='entry-content').find('a')['href']
            result_news.append({
                'title': title_news,
                'date': date_news,
                'text_news': text_news,
                'img_news': img_news,
                'href_news': href_news,
            })
    except FileNotFoundError:
        result_news = []
    return result_news


result_news = get_game_news(html_news)
