from sqlalchemy import JSON, Column, Integer, String

from db_tabletop import Base, engine

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


    def __repr__(self):
        return f'User {self.id}, {self.name}'

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)