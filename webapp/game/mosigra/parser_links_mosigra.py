import requests
from bs4 import BeautifulSoup as bs
import json
import re
from models import Game
from db_tabletop import db_session
from psycopg2._psycopg import IntegrityError


def get_html(url:str) -> str:
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False


def get_games_data(game_page:str) -> dict:
    game_data = {
        'name' : None,
        'numbers_of_players' : None,
        'age' : None,
        'brand' : None,
        'description' : None,
        'tags' : None,
        'image' : None
    }
    soup = bs(game_page, 'html.parser')
    game_data['name'] = soup.find('article', class_="product__article tabs-container").find('h1').text
    something = (soup.find(id="attributes", class_='tab-pane fade show').text).strip()
    while '\n\n' in something:
        something = something.replace('\n\n', '\n')
    something = list(something.split('\n'))
    if 'Возраст игроков' in something:
        ind = something.index('Возраст игроков')
        game_data['age'] = something[ind + 1]
    if 'Количество игроков' in something:
        ind = something.index('Количество игроков')
        game_data['numbers_of_players'] = something[ind + 1]
    if 'Производитель' in something:
        ind = something.index('Производитель')
        game_data['brand'] = something[ind + 1]
    try:
        game_data['description'] = re.sub("[\r\t]", '', soup.find(
            'div', class_="tab-content product-full-description"
        ).find('p').text.replace('\xa0', ' ')).strip('\n')

        if game_data['description'].strip('\n') == '':
            game_data['description'] = re.sub("[\r\t\n]", '', soup.find(
                'div', class_="tab-content product-full-description"
            ).find_all('p')[1].text.replace('\xa0', ' ')).strip('\n')

    except(AttributeError, IndexError):
        game_data['description'] = None
    tags_list = soup('a', class_="categories__link d-block mb-2")
    tags = [tag.text for tag in tags_list]
    game_data['tags'] = json.dumps(tags)
    game_data['image'] = soup.find('meta', property="og:image")['content']
    return game_data


if __name__ == '__main__':

    with open('links_list.txt', 'r') as links_file:
        lines = links_file.readlines()[:]
        for line in lines:
            if line:
                current_game = Game(**get_games_data(get_html(line)))
                try:
                    db_session.add(current_game)
                    db_session.commit()
                except IntegrityError:
                    db_session.rollback()
