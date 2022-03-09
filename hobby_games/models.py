from sqlalchemy import Column, Integer, String
from db import Base, engine

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    description = Column(String())
    number_of_players = Column(String())
    age = Column(Integer)
    brand = Column(String())
    image = Column(String())

    def __repr__(self) -> str:
        return f'Игра {self.name} - {self.brand}'


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    link = Column(String())
    status = Column(String())

    def __repr__(self) -> str:
        return f'Ссылка {self.link} - {self.status}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)