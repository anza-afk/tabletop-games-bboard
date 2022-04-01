from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from webapp.database import Base, engine, db, db_session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(), index=True, unique=True)
    password = Column(String())
    email = Column(String(), unique=True)
    role = Column(String())
    user_profile = relationship(
        'UserProfile',
        backref='user',
        uselist=False,
        lazy='joined'
    )
    user_meetings = relationship("MeetingUser", back_populates='user', lazy='joined')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'Пользователь {self.username} - {self.email}'


class UserProfile(db.Model, UserMixin):
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
        return f'Пользователь {self.name}'


class GameMeeting(db.Model, UserMixin):
    __tablename__ = 'game_meetings'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer(), ForeignKey('users.id'))
    game_name = Column(String(), index=True)
    create_date = Column(Date())
    number_of_players = Column(Integer())
    meeting_place = Column(String())
    meeting_date_time = Column(DateTime(timezone=True))
    description = Column(String())
    subscribed_players = Column(JSON)
    confirmed_players = Column(JSON)
    game_id = Column(Integer, ForeignKey('games.id'), index=True, nullable=True)
    user = relationship('User', backref='game_meetings', foreign_keys=[owner_id], lazy='joined')
    users = relationship('MeetingUser', lazy='joined')
    game = relationship("Game", lazy='subquery')

    def repr(self):
        return f'{self.user}\'s {GameMeeting.game_name}'

    @classmethod
    def active_games(cls, session):
        return session.query(cls).filter(cls.meeting_date_time > datetime.now())


class MeetingUser(db.Model):
    __tablename__ = "meeting_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    meeting_id = Column(Integer, ForeignKey('game_meetings.id'), index=True, nullable=False)
    confirmed = Column(Boolean, nullable=False)
    user = relationship("User", lazy='subquery')

    def get_meet(session, meeting_id):
        return session.query(MeetingUser).filter(MeetingUser.id == meeting_id).one()

    def confirm_user(self):
        self.confirmed = True

    def un_confirm_user(self):
        self.confirmed = False



class Game(db.Model):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    number_of_players = Column(String())
    age = Column(String())
    brand = Column(String())
    description = Column(String())
    tags = Column(JSON())
    image = Column(String())


class Link(db.Model):
    __tablename__ = 'links_from_hg'

    id = Column(Integer, primary_key=True)
    link = Column(String(), unique=True)
    status = Column(String())

    def __repr__(self) -> str:
        return f'Ссылка {self.link} - {self.status}'


class GameHg(db.Model):
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
