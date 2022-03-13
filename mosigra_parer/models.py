from sqlalchemy import JSON, Column, Integer, String

from mosigra.db_tabletop import Base, engine

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    number_of_players = Column(String())
    age = Column(String())
    brand = Column(String())
    description = Column(String())
    tags = Column(JSON())
    image = Column(String())

    def __init__(self, name, number_of_players, age, brand, description, tags, image):
        self.name = name
        self.number_of_players = number_of_players
        self.age = age
        self.brand = brand
        self.description = description
        self.tags = tags
        self.image = image


    def __repr__(self):
        return f'User {self.id}, {self.name}'

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)