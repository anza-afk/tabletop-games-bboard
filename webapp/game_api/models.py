from sqlalchemy import Column, Integer, String, JSON
from webapp.database import db

class Game(db.Model, Resource):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    number_of_players = Column(String())
    age = Column(String())
    brand = Column(String())
    description = Column(String())
    tags = Column(JSON())
    image = Column(String())

    @classmethod
    def get(cls, session, name=None):
        return session.query(cls).filter(cls.name == name)

    @classmethod
    def post(cls, id):
        pass

    @classmethod
    def put(cls, id):
        pass

    @classmethod
    def delete(cls, id):
        pass
