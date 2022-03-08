from importlib.resources import path
from requests import get, RequestException
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_html(url):
    try:
        result = get(url)
        result.raise_for_status()
        return result.text
    except(RequestException, ValueError):
        return False


def get_number_of_last_page_game_list(first_page):
    last_page_html = get_html(first_page)
    beautiful_html = BeautifulSoup(last_page_html, 'html.parser')
    last_page_url = beautiful_html.find('ul', class_='pagination').find('a', class_='last')['href']
    number_of_last_page = urlparse(last_page_url)[4].split('&')[0].split('=')[1]
    return number_of_last_page


def get_links_from_page(html):
    with open(html, "r", encoding="utf8") as f:
        html = f.read()
        beautiful_html = BeautifulSoup(html, 'html.parser')
        link = beautiful_html.find('div', class_='product-item__content').find('div', class_='image').find('a')['href']
        print(link)


def add_links_to_list(links):
    pass

    
if __name__ == "__main__":
    # number_of_last_page = get_number_of_last_page_game_list(https://hobbygames.ru/nastolnie?page=1&results_per_page=60&parameter_type=0)
    # for current_number_of_page in range(1, number_of_last_page + 1):
    #     html = get_html(f'https://hobbygames.ru/nastolnie?page={current_number_of_page}&parameter_type=0')
    #     links = get_links_from_page(html)
    #     add_links_to_list(links)

    
    links = get_links_from_page('hobby_games/links_of_page_game.html')

    # add_links_to_list(links)
