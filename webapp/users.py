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
    query = query.limit(page_limit)
    if page_number > 1:
        query = query.offset((page_number-1)*page_limit)
    return query


def add_user_to_wish_list(user_id, meet_id):
    """
    Если желающих играть еще нет - создается список в который помещается
    текущий пользователь. Если желающие есть, то текущий пользователь
    добавляется к ним.
    """
    with db_session() as session:
        meet = session.query(Meeting).filter(Meeting.id == meet_id).first()
        if not meet.wishing_to_play:
            meet.wishing_to_play = [user_id]
        if user_id not in meet.wishing_to_play:
            meet.wishing_to_play = meet.wishing_to_play + [user_id]
        session.commit()


def del_user_from_game(user_id, meet_id):
    """
    Если пользователь в списке желающих(или подтвержденных), то список преобразуется
    во множество, после чего из него удаляется пользователь и
    множество обратно преобразуется в список.
    """
    with db_session() as session:
        meet = session.query(Meeting).filter(Meeting.id == meet_id).first()
        if user_id in meet.wishing_to_play:
            meet.wishing_to_play = list(set(meet.wishing_to_play) - {user_id})
        elif user_id in meet.confirmed_players:
            meet.confirmed_players = list(set(meet.confirmed_players) - {user_id})
        session.commit()
