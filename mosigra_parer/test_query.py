from mosigra.db_tabletop import db_session
from models import Game
import json

games = db_session.query(Game.tags).limit(1)
for i in games:
    print(json.loads(i[0]))
