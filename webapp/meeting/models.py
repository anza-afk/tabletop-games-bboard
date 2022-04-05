from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from webapp.database import db
from flask_login import UserMixin
from datetime import datetime


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
        """
        Возвращает список игр с датой и временем больше, чем текущие.
        """
        return session.query(cls).filter(cls.meeting_date_time > datetime.now())

    @classmethod
    def join_meetings(cls, session, meeting_id):
        """
        Возвращает данные встречи по её id
        """
        return cls.active_games(session).filter(GameMeeting.id == meeting_id).one()

    @classmethod
    def owner_meetings(cls, session, user_id):
        """
        Возвращает список из активных встреч,созданные текущим пользователь
        """

        return cls.active_games(session).filter(cls.owner_id == user_id)

    @classmethod
    def sub_to_meetings(cls, session, user_id):
        """
        Возвращает список из активных встреч, на которые подписан текущий пользователь
        """
        return cls.active_games(session).join(cls.users).filter(MeetingUser.user_id == user_id)


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
        """
        Подтверждает пользователя для текущего экземляра встречи
        """
        self.confirmed = True

    def un_confirm_user(self):
        """
        Отменяет подтверждение пользователя для текущего экземляра встречи
        """
        self.confirmed = False
