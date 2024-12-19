
from sqlalchemy import Column, Integer, Date
from models.base import Base


class Protocol(Base):
    __tablename__ = 'protocols'
    id = Column(Integer, primary_key=True)
    date_p = Column(Date)
    location_id = Column(Integer)

