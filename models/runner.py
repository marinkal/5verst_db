
from sqlalchemy import Column, Integer, String
from models.base import Base


class Runner(Base):
    __tablename__ = 'runners'
    id = Column(Integer, primary_key=True)
    ident = Column(String)
    fio = Column(String)

