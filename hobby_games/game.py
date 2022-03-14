from bs4 import BeautifulSoup as bs


class Card_game():
    def __init__(self, html, link_id) -> None:
        self.html = bs(html, 'html.parser')
        self.link_id = link_id
        try:
            self.name = self.html.find('div', class_='product-info__main').text.strip()
        except AttributeError:
            self.name = None

        try:
            self.description = self.html.find('div', class_='desc-text').find('p').text.strip()
        except AttributeError:
            self.description = None

        try:
            self.number_of_players = self.html.find('div', class_='players').text.strip()
        except AttributeError:
            self.number_of_players = None

        try:
            self.age = self.html.find('div', class_='age').text.strip()
        except AttributeError:
            self.age = None

        try:
            self.brand = ''.join(
                self.html.find('a', class_='manufacturers__value').text.split()
                )
        except AttributeError:
            self.brand = None

        try:
            self.image = self.html.find('a', class_='lightGallery')['href']
        except AttributeError:
            self.image = None

        try:
            self.tags = ', '.join([
                a.text.strip() for a in
                self.html.find('div', class_='tags').find_all('a')
                ])
        except AttributeError:
            self.tags = None

    def give_game_params(self) -> dict:
        if self.name is None:
            return {}

        params = {
            'name': self.name,
            'link_id': self.link_id,
            'description': self.description,
            'number_of_players': self.number_of_players,
            'age': self.age,
            'brand': self.brand,
            'image': self.image,
            'tags': self.tags,
        }
        return params






# def get_game_params(page_of_game):
#     """
#     Возвращает словарь параметров игры.
#     """
#     with open(page_of_game, "r", encoding="utf8") as f:  # 
#         bs_html = bs(f, 'html.parser')
#         params = {
#             'name': bs_html.find('div', class_='product-info__main').text.strip(),
#             'description': bs_html.find('div', class_='desc').text.strip(),
#             'number_of_players': bs_html.find('div', class_='players').text.strip(),
#             'age': int(''.join([ch for ch in bs_html.find('div', class_='age').text.strip() if ch.isdigit()])),
#             'brand': ''.join(bs_html.find('a', class_='manufacturers__value').text.split()),
#             'image': bs_html.find('a', class_='lightGallery')['href'],
#         }

#         try:
#             params['tags'] =  ' '.join([a.text.strip() for a in bs_html.find('div', class_='tags').find_all('a')])
#         except AttributeError:
#             print('tags недоступны')
#             params['tags'] = None

#     return params