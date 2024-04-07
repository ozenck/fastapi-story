from apps.story.models import Story
from apps.story.schemas import StoryCreate
from fastapi.exceptions import HTTPException

async def create_story_record(story: StoryCreate, db):
    try:
        new_story = Story(app_id=story.app_id, metadata_=story.metadata)
        db.add(new_story)
        db.commit()
        return new_story
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Story couldn't save. Error: {ex}")
