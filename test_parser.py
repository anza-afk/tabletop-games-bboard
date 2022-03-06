from bs4 import BeautifulSoup

html_news = 'news_game.html'

def get_game_news(html_news: str) -> list[dict]:
    with open("news_game.html", "r", encoding="utf8") as f:
        html = f.read()
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
    return result_news


result_news = get_game_news(html_news)
