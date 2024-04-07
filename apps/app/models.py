from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class App(Base):
    __tablename__ = "apps"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, index=True)
    stories = relationship("Story", back_populates="app")
    events = relationship("Event", back_populates="app")
