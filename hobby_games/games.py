from links import get_html


def get_game_params():
    """
    Возвращает список json'ов содержащих данные по отдельной игре.
    """
    pass


def add_games_to_db():
    """
    Записывает в ДБ данные игр на основании полученных json'ов.
    """
    pass


if __name__ == '__main__':
    # with open('hobby_games/links_of_page', 'r', encoding='utf8') as f:
    #     for link in f:
    #         page_of_game_html = get_html(link)
    #         get_game_params(page_of_game_html)

    game = get_html('https://hobbygames.ru/nemezida')
    with open('hobby_games/game', "w", encoding="utf8") as f:
        f.write(game)
