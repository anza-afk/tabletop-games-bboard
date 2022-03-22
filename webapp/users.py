from webapp.db import db_session
from webapp.models import User, UserProfile
from webapp.models import Meeting
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
    except sqlalchemy.exc: #  sqlalchemy.exc не обрабатываются, нужно понять как обрабатывать
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
        print(profile.surname)
        session.commit()
        

def join_profile(user_id):
    with db_session() as session:
        result = session.query(UserProfile).filter(UserProfile.owner_id == user_id).first()
    return result


def add_meeting(new_meeting: Meeting) -> bool:
    """
    Записывает данные новой встречи в БД.
    Возвращает результат записи.
    """
    #try:
    with db_session() as session:
        session.add(new_meeting)
        session.commit()
    return True
    #except sqlalchemy.exc: #  sqlalchemy.exc не обрабатываются, нужно понять как обрабатывать
    #    return False

def paginate(query, page_number, page_limit):
    if page_number > 1:
        query = query.offset(page_number*page_limit)
    query = query.limit(page_limit)
    return query.all()