from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from webapp.database import Base, engine, db
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


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)