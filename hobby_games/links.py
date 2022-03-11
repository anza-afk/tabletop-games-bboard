from requests import get, RequestException
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from db import db_session
from models import Link
from sqlalchemy.exc import IntegrityError


def get_html(url: str) -> str:
    """
    Возвращает html страницу полученную по ссылке.
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
    last_page_url = beautiful_html.find(
        'ul', class_='pagination'
        ).find('a', class_='last')['href']
    number_of_last_page = int(
        urlparse(last_page_url)[4].split('&')[0].split('=')[1]
        )
    return number_of_last_page


def get_links_from_page(html: str) -> list[dict]:
    """
    Возвращает список словарей с сылками на игры, которые размещены на
    переданной странице.
    """
    beautiful_html = BeautifulSoup(html, 'html.parser')
    games_links = [
        {'link': a['href'], 'status': 'not collected'}
        for a in beautiful_html.find_all('a', class_='name')
    ]
    return games_links


def add_links_to_db(links: list) -> None:
    """
    Записыват ссылки на игры в БД.
    """
    # db_session.bulk_insert_mappings(Link, links)
    # db_session.commit()
    for href in links:
        try:
            db_session.add(Link(
                link=href['link'],
                status=href['status']
            ))
            db_session.commit()
        except IntegrityError:
            print(href)
            db_session.rollback()


if __name__ == "__main__":
    number_of_last_page = get_number_of_last_page_game_list('https://hobbygames.ru/nastolnie?page=1&results_per_page=60&sort=name&order=ASC&parameter_type=0')
    for current_number_of_page in range(1, number_of_last_page + 1):
        html = get_html(f'https://hobbygames.ru/nastolnie?page={current_number_of_page}&results_per_page=60&sort=name&order=ASC&parameter_type=0')
        if html:
            links = get_links_from_page(html)
            add_links_to_db(links)
