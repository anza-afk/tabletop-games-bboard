from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from sqlalchemy import Column, Integer, String, JSON
from webapp.database import db

app = Flask(__name__)
api = Api(app)


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
        if session.query(cls).filter(cls.name == name):
            return jsonify(session.query(cls).filter(cls.name == name)), 200
        return "Game not found", 404

    @classmethod
    def post(cls, session, name):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("number_of_players")
        parser.add_argument("age")
        parser.add_argument("brand")
        parser.add_argument("description")
        parser.add_argument("tags")
        parser.add_argument("image")
        params = parser.parse_args()
        if session.query(cls).filter(cls.name == name):
            return f"Game with name {name} already exists", 400
        new_game = Game(
            name=params["name"],
            number_of_players=params["number_of_players"],
            age=params["age"],
            brand=params["brand"],
            description=params["description"],
            tags=params["tags"],
            image=params["image"]
        )
        session.add(new_game)
        session.commit()
        return jsonify(new_game), 201

    @classmethod
    def put(cls, session, name):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("number_of_players")
        parser.add_argument("age")
        parser.add_argument("brand")
        parser.add_argument("description")
        parser.add_argument("tags")
        parser.add_argument("image")
        params = parser.parse_args()
        game = session.query(cls).filter(cls.name == name)
        if game:
            game.name = params["name"],
            game.number_of_players = params["number_of_players"],
            game.age = params["age"],
            game.brand = params["brand"],
            game.description = params["description"],
            game.tags = params["tags"],
            game.image = params["image"]
            return jsonify(game), 200
        new_game = Game(
            name=params["name"],
            number_of_players=params["number_of_players"],
            age=params["age"],
            brand=params["brand"],
            description=params["description"],
            tags=params["tags"],
            image=params["image"]
        )
        session.add(new_game)
        session.commit()
        return jsonify(new_game), 201

    @classmethod
    def delete(cls, session, name):
        game = session.query(cls).filter(cls.name == name)
        session.delete(game)
        session.commit()

        return f"Gmae {name} is deleted.", 200


api.add_resource(Game, )  # с этим не понимаю, URI тут нет, эндпоинтов нет. Или надо в эндпоинты jsonify и методы положить?

if __name__ == '__main__':
    app.run(debug=True)
