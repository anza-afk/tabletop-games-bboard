from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
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
    id_user_create = Column(Integer(), ForeignKey('users.id'))
    game_name = Column(String())
    date_create = Column(Date())
    number_of_players = Column(Integer())
    meeting_place = Column(String())
    date_meeting = Column(Date())
    time_meeting = Column(Time())
    description = Column(String())
    wishing_to_play = Column(JSON)
    confirmed_players = Column(JSON)
    user = relationship('User', backref='meetings')

    def meetings_count(self):
        return MeetingForPlay.query.all()

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
