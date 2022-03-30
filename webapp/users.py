from flask import Flask
from webapp.database import db_session
from webapp.models import Game, User, UserProfile,  GameMeeting, MeetingUser
from flask_wtf import FlaskForm
import sqlalchemy.exc


def add_user(new_user: User) -> bool:
    """
    Записывает данные нового пользователя в БД.
    Возвращает результат записи.
    """
    try:
        with db_session() as session:
            session.add(new_user)
            session.commit()
        return True
    except sqlalchemy.exc:  # sqlalchemy.exc не обрабатываются, нужно понять как обрабатывать
        return False


def add_profile(new_profile: UserProfile) -> None:
    with db_session() as session:
        session.add(new_profile)
        session.commit()


def update_profile(form, user_id) -> None:
    with db_session() as session:
        profile = session.query(UserProfile).filter(UserProfile.owner_id == user_id.id).first()
        profile_email = session.query(User).filter(User.email == user_id.email).first()
        profile_email.email = form['email'].data
        profile.owner_id = user_id.id,
        profile.name = form['name'].data,
        profile.surname = form['surname'].data,
        profile.country = form['country'].data,
        profile.city = form['city'].data,
        profile.favorite_games = form['favorite_games'].data,
        profile.desired_games = form['desired_games'].data,
        profile.about_user = form['about_user'].data
        session.commit()


def update_meeting(form: FlaskForm, meeting_id: int) -> None:
    with db_session() as session:
        meet = session.query(GameMeeting).filter(GameMeeting.id == meeting_id).first()
        meet.game_name = form['game_name'].data
        meet.number_of_players = form['number_of_players'].data
        meet.meeting_place = form['meeting_place'].data
        meet.meeting_date_time = f"{form['date_meeting'].data} {form['time_meeting'].data}"
        meet.description = form['description'].data
        session.commit()


def join_profile(user_id):
    with db_session() as session:
        return session.query(UserProfile).filter(UserProfile.owner_id == user_id).first()


def add_meeting(new_meeting: GameMeeting) -> bool:
    """
    Записывает данные новой встречи в БД.
    Возвращает результат записи.
    """
    # try:
    with db_session() as session:
        session.add(new_meeting)
        session.commit()
    return True
    # except sqlalchemy.exc: #  sqlalchemy.exc не обрабатываются, нужно понять как обрабатывать
    #    return False


def paginate(query, page_number, page_limit):
    query = query.limit(page_limit)
    if page_number > 1:
        query = query.offset((page_number - 1) * page_limit)
    return query


def join_meets(meet_id):
    with db_session() as session:
        return session.query(GameMeeting).filter(GameMeeting.id == meet_id).one()


def owner_meetings(user_id):
    with db_session() as session:
        return session.query(GameMeeting).filter(GameMeeting.owner_id == user_id).all()


def sub_to_meetings(user_id):
    with db_session() as session:
        return session.query(GameMeeting).join(GameMeeting.users).filter(MeetingUser.user_id == user_id).all()

def game_full_info(game_id):
    with db_session() as session:
        return session.query(Game).filter(Game.id == game_id).first()
