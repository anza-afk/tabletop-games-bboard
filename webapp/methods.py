from webapp.user.models import User, UserProfile
from webapp.meeting.models import GameMeeting
from webapp.location.models import City
from flask_wtf import FlaskForm
import requests
import json


def update_profile(session, form, user_id) -> None:
    """
    Обновляет данные профиля в БД
    """
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


def update_meeting(session, form: FlaskForm, meeting_id: int) -> None:
    """
    Обновляет данные встречи в БД
    """
    db_city = session.query(City).filter(City.name == form['meeting_city'].data).first()
    city_id = db_city.id if db_city else None
    meet = session.query(GameMeeting).filter(GameMeeting.id == meeting_id).first()
    meet.game_name = form['game_name'].data
    meet.number_of_players = form['number_of_players'].data
    meet.city_name = form['meeting_city'].data
    meet.city_id = city_id,
    meet.meeting_place = form['meeting_place'].data
    meet.meeting_date_time = f"{form['date_meeting'].data} {form['time_meeting'].data}"
    meet.description = form['description'].data
    session.commit()


def add_meeting(session, new_meeting: GameMeeting) -> bool:
    """
    Записывает данные новой встречи в БД.
    Возвращает результат записи.
    """
    # try:
    session.add(new_meeting)
    session.commit()
    return True
    # except sqlalchemy.exc: #  sqlalchemy.exc не обрабатываются, нужно понять как обрабатывать
    #    return False


def delete_meeting(session, meeting_id: int) -> None:
    meet = session.query(GameMeeting).filter(GameMeeting.id == meeting_id).first()
    print(meet.deleted)
    meet.deleted = True
    print(meet.deleted)
    print(meet.id,'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    session.commit()


def paginate(query, page_number, page_limit):
    """
    Почти универсальная пагинация
    """
    query = query.limit(page_limit)
    if page_number > 1:
        query = query.offset((page_number - 1) * page_limit)
    return query


def get_news():
    try:
        return json.loads(requests.get('http://news:5001/news/').text)['News']
    except requests.exceptions.ConnectionError:
        return []
