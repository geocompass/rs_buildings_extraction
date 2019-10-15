from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class Buia(Base):
    gid = Column(Integer, primary_key=True)
    CNAME = Column(String(48))
    LEVEL = Column(String(16))
    geom = Column(Text)
