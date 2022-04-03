
from flask import session
from models import Link, Game
from db import db_session
from sqlalchemy import func, desc

games = db_session.query(Game.tags).limit(1)
print(games)
print([tags for tags in games])
# print(db_session.query(Link.link).count())

# links = db_session.query(Link.link, func.count(Link.link)).group_by(Link.link).having(func.count(Link.link) == 1)

# print([link for link in links])
# links = db_session.query(Link.link).all()
# print(links)

# links = db_session.query(Link.link, Link.id).filter(Link.status == 'not collected')
# print([(link[1]) for link in links])
