from sqlalchemy import Column, Integer, String, Float
from db import Base


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String)
    title = Column(String)
    description = Column(String)
    price = Column(Float)