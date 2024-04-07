from pydantic import BaseModel

class StoryCreate(BaseModel):
    app_id: int
    metadata: dict
