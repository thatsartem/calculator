from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY


from database import Base


class Directions(Base):
    __tablename__ = 'directions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    university = Column(String)
    code = Column(String)
    form = Column(String)
    subjects = Column(ARRAY(Integer))
    budget_seats = Column(Integer)
    paid_seats = Column(Integer, default=0)
    passing_score = Column(Integer)
    tuition_fee = Column(Integer, default=0)
    mean = Column(Integer, default=-1)
    dispersion = Column(Integer, default=-1)
    link = Column(String)