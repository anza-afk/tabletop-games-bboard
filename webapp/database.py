from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from webapp.config import SQLALCHEMY_DATABASE_URI as DB
from flask_sqlalchemy import SQLAlchemy

engine = create_engine(DB, pool_size=3, max_overflow=0)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
db = SQLAlchemy()
Base.query = db_session.query_property()
