from tabnanny import check
from tkinter.messagebox import NO
from webapp.db import db_session
from webapp.models import User

def check_user(new_user_email):
    return db_session.query(User.email).filter(User.email == new_user_email).count()

def add_user(new_user: User) -> None:
    db_session.add(new_user)
    db_session.commit()

