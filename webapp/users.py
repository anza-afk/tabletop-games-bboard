from webapp.db import db_session
from webapp.models import User, User_profile

def check_user(new_user_email):
    return db_session.query(User.email).filter(User.email == new_user_email).count()

def add_user(new_user: User) -> None:
    db_session.add(new_user)
    db_session.commit()

def add_profile(new_profile: User_profile) -> None:
    db_session.add(new_profile)
    db_session.commit()