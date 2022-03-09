from importlib.resources import path
from tkinter.messagebox import NO
from requests import get, RequestException
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_html(url: str) -> str: 
    """
    Возвращает html страницу полученную по переданному адресу.
    """
    try:
        result = get(url)
        result.raise_for_status()
        return result.text
    except(RequestException, ValueError):
        return False


def get_number_of_last_page_game_list(first_page: str) -> int:
    """
    Возвращает номер последней страницы, содержащей игры во вкладке
    настольных игр.
    """
    last_page_html = get_html(first_page)
    beautiful_html = BeautifulSoup(last_page_html, 'html.parser')
    last_page_url = beautiful_html.find('ul', class_='pagination').find('a', class_='last')['href']
    number_of_last_page = int(urlparse(last_page_url)[4].split('&')[0].split('=')[1])
    return number_of_last_page


def get_links_from_page(html: str) -> list:
    """
    Возвращает список ссылок на игры, которые размещены на
    переданной странице.
    """
    with open(html, "r", encoding="utf8") as f:
        html = f.read()
        beautiful_html = BeautifulSoup(html, 'html.parser')
        games_links = [a['href'] for a in beautiful_html.find_all('a', class_='name')]
        return games_links


def add_links_to_list(links: list) -> None:
    """
    Записыват в файл полученные ссылки,
    каждую с новой строки.
    """
    with open('hobby_games/links_of_page', "a", encoding="utf8") as f:
        for link in links:
            f.write(f'{link}\n')

    
if __name__ == "__main__":
    # number_of_last_page = get_number_of_last_page_game_list(https://hobbygames.ru/nastolnie?page=1&results_per_page=60&parameter_type=0)
    # for current_number_of_page in range(1, 2):  # number_of_last_page + 1
    #     html = get_html(f'https://hobbygames.ru/nastolnie?page={current_number_of_page}&parameter_type=0')
    #     links = get_links_from_page(html)
    #     add_links_to_list(links)

    
    links = get_links_from_page('hobby_games/links_of_page_game.html')
    add_links_to_list(links)
