from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('postgresql://oxzjtwvr:fbmGCjpoShzjEqJktDdaQsTC8TUK-Shn@balarama.db.elephantsql.com/oxzjtwvr')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()