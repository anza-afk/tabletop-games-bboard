from flask import request
from requests import get, RequestException, Session
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from db import db_session
from models import Link
from sqlalchemy.exc import IntegrityError


BASE_URL = 'https://hobbygames.ru/nastolnie?page={0}&results_per_page=60&sort=name&order=ASC&parameter_type=0'


def get_html(url: str, session: Session) -> str:
    """
    Возвращает soup страницу полученную по ссылке.
    """
    try:
        result = session.get(url)
        result.raise_for_status()
        return result.text
    except(RequestException, ValueError):
        print(f'Не удалось получить страницу: {url}')


def get_number_of_last_page_game_list(first_page: str, session: Session) -> int:
    """
    Возвращает номер последней страницы, содержащей игры во вкладке
    настольных игр.
    """
    last_page_html = get_html(first_page, session)
    soup = BeautifulSoup(last_page_html, 'html.parser')
    last_page_url = soup.find(
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
    soup = BeautifulSoup(html, 'html.parser')
    games_links = [
        {'link': a['href'], 'status': 'not collected'}
        for a in soup.find_all('a', class_='name')
    ]
    return games_links


def add_links_to_db(links: list) -> None:
    """
    Записыват ссылки на игры в БД.
    """
    for link_game in links:
        try:
            db_session.add(Link(
                link=link_game['link'],
                status=link_game['status']
            ))
            db_session.commit()
        except IntegrityError:
            db_session.rollback()


if __name__ == "__main__":
    current_session = Session()
    number_of_last_page = get_number_of_last_page_game_list(BASE_URL.format(1), current_session)
    for current_number_of_page in range(1, 2):  # number_of_last_page + 1
        html = get_html(BASE_URL.format(current_number_of_page), current_session)
        if html:
            links = get_links_from_page(html)
            add_links_to_db(links)
