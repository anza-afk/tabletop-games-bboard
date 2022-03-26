from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import relationship
from webapp.db import Base, engine, db_session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(Base, UserMixin):
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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self) -> str:
        return f'Пользователь {self.username} - {self.email}'


class UserProfile(Base, UserMixin):
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


class GameMeeting(Base, UserMixin):
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
    user = relationship('User', backref='game_meetings', foreign_keys=[owner_id],  lazy='joined')

    def add_user(self, user_id: int) -> None:
        """
        Добавляет пользователя в список желающих принять участие.
        """
        if user_id not in self.wishing_to_play:
            self.wishing_to_play = self.wishing_to_play + [user_id]

    def del_user(self, user_id: int, owner_id=None) -> None:
        """
        Удаляет пользователя из списка желающих или списка
        подтвержденных участников.
        """ 
        if user_id in self.wishing_to_play:
            self.wishing_to_play = list(set(self.wishing_to_play) - {user_id})
        elif (user_id in self.confirmed_players) or (owner_id and owner_id == self.owner_id):
            self.confirmed_players = list(set(self.confirmed_players) - {user_id})

    def meetings_count(self):
        return f'{self.user}\'s {GameMeeting.game_name}'

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
