from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class PredictBuildings(Base):
    gid = Column(Integer, primary_key=True)
    geom = Column(Text)
