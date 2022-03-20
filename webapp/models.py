from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from webapp.db import Base, engine
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(), index=True, unique=True)
    password = Column(String())
    email = Column(String(), unique=True)
    role = Column(String())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'Пользователь {self.username} - {self.email}'


class User_profile(Base, UserMixin):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer(), ForeignKey('users.id'), unique=True)
    name = Column(String())
    surname = Column(String())
    country = Column(String())
    city = Column(String())
    favorite_games = Column(String())
    desired_games = Column(String())
    about_user = Column(String())

    def __repr__(self) -> str:
        return f'Пользователь {User.username} - {User.email}'


class MeetingForPlay(Base, UserMixin):
    __tablename__ = 'meeting'

    id = Column(Integer, primary_key=True)
    number_of_players = Column(Integer())
    meeting_place = Column(String())
    desc = Column(String())
    wishing_to_play = Column(JSON)
    confirmed_players = Column(JSON)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
