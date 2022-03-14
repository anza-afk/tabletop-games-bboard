from links import get_html
from db import db_session
from models import Game, Link
from game import CardGame


def add_games_to_db(games_params: list[dict]) -> None:
    """
    Записывает в ДБ полученный список игр с параметрами,
    которые содержатся в словарях.
    """
    db_session.bulk_insert_mappings(Game, games_params)
    db_session.commit()


def get_links_to_collect() -> list[tuple]:
    """
    Возвращает список кортежей со значениями
    неопрошенных ссылок и pk.
    """
    links = db_session.query(Link.link, Link.id).filter(Link.status == 'not collected')
    return [(link[0], link[1]) for link in links]


if __name__ == '__main__':
    games_params = []

    for link in get_links_to_collect():
        page_of_game_html = get_html(link[0])
        if not page_of_game_html:
            continue
        game = CardGame(page_of_game_html, link[1])
        if not game:
            continue
        game_params = game.give_game_params()
        games_params.append(game_params)

    add_games_to_db(games_params)
