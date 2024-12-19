
from sqlalchemy import Column, Integer, String
from models.base import Base


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
