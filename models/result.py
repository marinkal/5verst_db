
from sqlalchemy import Column, Integer
from models.base import Base


class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    protocol_id = Column(Integer)
    place_row = Column(Integer)
    runner_id = Column(Integer)
    category_id = Column(Integer, nullable=True)
    result_time = Column(Integer, nullable=True)


