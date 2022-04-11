from sqlalchemy import Column, Integer, String, DateTime
from webapp.database import db


class News(db.Model):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    author = Column(String, nullable=False)
    published = Column(DateTime(timezone=True), nullable=False)
    content = Column(String, nullable=True)
    image = Column(String, nullable=True)

    def __repr__(self):
        return '<News {}>'.format(self.title)
