from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


class JourneyStage(BaseModel):
    stage_name: str
    description: str
    challenges: list


class JourneyStart(BaseModel):
    protagonist_desire: str
    helper_description: str



Base = declarative_base()


class Journey(Base):
    __tablename__ = 'journeys'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, nullable=False)
    stage = Column(String)
    result = Column(String)
    start_data = Column(String)
    journey_data = Column(String)
    challenge_data = Column(String)
    return_data = Column(String)