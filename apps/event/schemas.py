from pydantic import BaseModel
from datetime import date

# class EventCreate(BaseModel):
#     app_id: int
#     story_id: int
#     date: date
#     type: str
#     user_id: int
#     count: int

class EventPostRequest(BaseModel):
    story_id: int
    event_type: str
    user_id: int
