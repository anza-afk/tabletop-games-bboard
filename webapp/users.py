from webapp.db import db_session
from webapp.models import User, User_profile
from flask_login import current_user

def check_user(new_user_email):
    return db_session.query(User.email).filter(User.email == new_user_email).count()

def add_user(new_user: User) -> None:
    db_session.add(new_user)
    db_session.commit()
    db_session.close()
    

def add_profile(new_profile: User_profile) -> None:
    db_session.add(new_profile)
    db_session.commit()
    db_session.close()


def update_profile(form, user_id) -> None:
    profile = db_session.query(User_profile).filter(User_profile.owner_id == user_id.id).first()
    profile_email = db_session.query(User).filter(User.email == user_id.email).first()
    profile_email.email = form['email'].data
    profile.owner_id = user_id.id,
    profile.name=form['name'].data,
    profile.surname=form['name'].data,
    profile.country=form['country'].data,
    profile.city=form['city'].data,
    profile.favorite_games=form['favorite_games'].data,
    profile.desired_games=form['desired_games'].data,
    profile.about_user=form['about_user'].data
    print(profile.surname)
    db_session.commit()
    db_session.close()   
    

def join_profile(user_id):
    result = db_session.query(User_profile).filter(User_profile.owner_id == user_id).first()
    db_session.close()
    return result