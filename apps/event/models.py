from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, ForeignKey("apps.id"))
    story_id = Column(Integer, ForeignKey("stories.story_id"))
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    type = Column(String)
    count = Column(Integer, default=0)
    app = relationship("App", back_populates="events")
    stories = relationship("Story", back_populates="events")
    users = relationship("User", back_populates="events")

    __table_args__ = (
        UniqueConstraint('app_id', 'story_id', 'type', 'date', 'user_id', name='uix_app_id_story_id_type_date_user_id'),)
