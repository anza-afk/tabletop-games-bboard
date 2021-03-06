from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from db import Base, engine


class Link(Base):
    __tablename__ = 'links_from_hg'

    id = Column(Integer, primary_key=True)
    link = Column(String(), unique=True)
    status = Column(String())

    def __repr__(self) -> str:
        return f'Ссылка {self.link} - {self.status}'


class GameHg(Base):
    __tablename__ = 'games_hg'

    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey(Link.id))
    name = Column(String())
    description = Column(String())
    number_of_players = Column(String())
    age = Column(String())
    brand = Column(String())
    image = Column(String())
    tags = Column(JSON)

    def __repr__(self) -> str:
        return f'Игра {self.name} - {self.brand}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
