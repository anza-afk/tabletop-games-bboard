from bs4 import BeautifulSoup as bs


class CardGame:
    def __new__(cls, html, link_id):
        """
        Переопределенный метод создания экземпляра класса:
        Если не получается найти название игры, то экземпляр
        не будет создан, если найден - отработает базовый
        метод __new__.
        """
        soup = bs(html, 'html.parser')
        if not soup.find('div', class_='product-info__main'):
            return None
        else:
            return super().__new__(cls)

    def __init__(self, html, link_id) -> None:
        self.soup = bs(html, 'html.parser')
        self.link_id = link_id
        try:
            self.name = self.soup.find('div', class_='product-info__main').text.strip()
        except AttributeError:
            self.name = None

        try:
            self.description = self.soup.find('div', class_='desc-text').find('p').text.strip()
        except AttributeError:
            self.description = None

        try:
            self.number_of_players = self.soup.find('div', class_='players').text.strip()
        except AttributeError:
            self.number_of_players = None

        try:
            self.age = self.soup.find('div', class_='age').text.strip()
        except AttributeError:
            self.age = None

        try:
            self.brand = ''.join(
                self.soup.find('a', class_='manufacturers__value').text.split()
                )
        except AttributeError:
            self.brand = None

        try:
            self.image = self.soup.find('a', class_='lightGallery')['href']
        except AttributeError:
            self.image = None

        try:
            self.tags = [
                a.text.strip() for a in
                self.soup.find('div', class_='tags').find_all('a')
                ]
        except AttributeError:
            self.tags = None

    def give_game_params(self) -> dict:
        """
        Возвращает словарь с параметрами игры.
        """
        return {
            'name': self.name,
            'link_id': self.link_id,
            'description': self.description,
            'number_of_players': self.number_of_players,
            'age': self.age,
            'brand': self.brand,
            'image': self.image,
            'tags': self.tags,
        }
