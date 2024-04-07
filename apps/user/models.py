from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mail = Column(String)
    events = relationship("Event", back_populates="users")
