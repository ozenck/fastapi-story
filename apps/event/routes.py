from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from core.database import get_db
from fastapi.responses import Response
from core.utils import date_validator
from core.redis_handler import RedisSingleton
from apps.event.schemas import EventPostRequest
from apps.event.services import create_event_record, get_events_record

events_router = APIRouter(
    prefix="/event",
    tags=["Event"],
    responses={404: {"description": "Not found"}},
)

redis_cache = RedisSingleton()


async def event_to_dict(event_instance):
    event_dict = {
        "app_id": event_instance.id,
        "date": event_instance.date.isoformat(),
        "count": event_instance.count,
        "story_id": event_instance.story_id,
        "story_metadata": event_instance.stories.metadata_,
        "user": {"id": event_instance.user_id, "name": event_instance.users.name, "mail": event_instance.users.mail}
    }
    return event_dict


@events_router.post("/{token}", summary="Create Event")
@redis_cache.cache(timeout=60)
async def create_events(request: Request, token: str, event_data: EventPostRequest, db: Session = Depends(get_db)):
    """
        Endpoint to creates new event related with the app token
    """
    return await create_event_record(token, event_data, db)

@events_router.get("/{token}", summary="Get Events")
@redis_cache.cache(timeout=60)
async def get_events(request: Request, token: str, date: str = Depends(date_validator), db: Session = Depends(get_db)):
    """
        Endpoint to get events according to app token and specific day
    """
    result = await get_events_record(token, date, db)
    if result:
        result_dict = [await event_to_dict(ev) for ev in result]
        return result_dict
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    