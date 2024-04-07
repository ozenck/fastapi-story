from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.orm import Session, joinedload
from core.database import get_db
from fastapi.responses import Response
from apps.app.models import App
import time
from core.redis_handler import RedisSingleton


stories_router = APIRouter(
    prefix="/stories",
    tags=["Story"],
    responses={404: {"description": "Not found"}},
)

redis_cache = RedisSingleton()

@stories_router.get("/{token}", summary="Story Metadata API ORM Join", status_code=status.HTTP_200_OK)
@redis_cache.cache(timeout=60)
async def get_story_metadata(request: Request, token: str, db: Session = Depends(get_db)):
    """
        This api returns the metadata according to app token
    """
    app = db.query(App).options(joinedload(App.stories)).filter(App.token == token).first()
    if not app:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return {
        "app_id": app.id,
        "ts": int(time.time()),
        "metadata": [ {"id": story.story_id, "metadata": story.metadata_.get("img")} for story in app.stories ]
    }
