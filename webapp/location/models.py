from sqlalchemy import Column, Integer, String, ForeignKey
from webapp.database import db


class Country(db.Model):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String())


class City(db.Model):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey(Country.id))
    name = Column(String())
