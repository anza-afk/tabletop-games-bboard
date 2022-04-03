from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base, engine, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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
    avatar = Column(String())

    def __repr__(self) -> str:
        return f'Пользователь {self.name}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
