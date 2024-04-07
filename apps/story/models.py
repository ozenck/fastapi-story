from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Story(Base):
    __tablename__ = "stories"
    story_id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, ForeignKey("apps.id"))
    metadata_ = Column("metadata", JSON) # 'metadata' attribute name is reserved
    app = relationship("App", back_populates="stories")
    events = relationship("Event", back_populates="stories")
