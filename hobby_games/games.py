from links import get_html
from bs4 import BeautifulSoup as bs
import json


def get_game_params(page_of_game):
    """
    Возвращает список json'ов содержащих данные по отдельной игре.
    """
    with open(page_of_game, "r", encoding="utf8") as f:
        bs_html = bs(f, 'html.parser')
        params = {
            'name': bs_html.find('div', class_='product-info__main').text.strip(),
            'description': bs_html.find('div', class_='desc').text.strip(),
            'number_of_players': bs_html.find('div', class_='players').text.strip(),
            'age': int(''.join([ch for ch in bs_html.find('div', class_='age').text.strip() if ch.isdigit()])),
            'brand': bs_html.find('a', class_='manufacturers__value').text.split(),
            'image': bs_html.find('a', class_='lightGallery')['href'],
        }

        try:
            params['tags'] =  [a.text.strip() for a in bs_html.find('div', class_='tags').find_all('a')]
        except AttributeError:
            print('tags недоступны')
            params['tags'] = []

    return params

def add_games_to_db(game_params):
    """
    Записывает в ДБ данные игр на основании полученных json'ов.
    """
    with open('hobby_games/gemes_params', 'a', encoding='utf-8') as f:
        json.dump(game_params, f, ensure_ascii = False)


if __name__ == '__main__':
    # with open('hobby_games/links_of_page', 'r', encoding='utf8') as f:
    #     for link in f:
    #         page_of_game_html = get_html(link)
    #         get_game_params(page_of_game_html)

    # game = get_html('https://hobbygames.ru/nemezida')
    # with open('hobby_games/game', "w", encoding="utf8") as f:
    #     f.write(game)

    game_params = get_game_params('hobby_games/game')
    print(game_params)
    add_games_to_db(game_params)
