from fastapi import status
from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from apps.event.models import Event
from fastapi.exceptions import HTTPException
from datetime import date
from apps.app.models import App
from apps.user.models import User
from apps.event.models import Event
from fastapi.responses import Response
from apps.event.schemas import EventPostRequest


async def create_event_record(token: str, ev: EventPostRequest, db):
    try:
        today = date.today().isoformat()
        app = db.query(App).options(joinedload(App.stories)).filter(App.token == token).first()
        if not app:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        user = db.query(User).filter(User.id == ev.user_id).first()
        if not user:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        event = db.query(Event).filter(Event.app_id == app.id).filter(
            and_(
            Event.story_id == ev.story_id,
            Event.type == ev.event_type,
            Event.date == today,
            Event.user_id == ev.user_id)
            ).first()
        if event:
            event.count +=1
            event.user_id = ev.user_id
            db.commit()
            return Response(content=f"Event Updated. app:{app.id}, story: {event.story_id}, type: {event.type}, user_id: {event.user_id} count: {event.count}", status_code=status.HTTP_200_OK)
        else: 
            new_event = Event(app_id=app.id, 
                        story_id=ev.story_id,
                        date=today,
                        type=ev.event_type,
                        user_id=ev.user_id,
                        count=1)
            db.add(new_event)
            db.commit()
            return Response(content=f"Event Created. app:{app.id}, story: {new_event.story_id}, type: {new_event.type}, user_id: {new_event.user_id} count: {new_event.count}", status_code=status.HTTP_201_CREATED)
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Event couldn't save. Error: {ex}")

async def get_events_record(token: str, date: date, db):
    try:
        app = db.query(App).options(joinedload(App.stories)).filter(App.token == token).first()
        if not app:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        event = db.query(Event).filter(
            and_(
            Event.app_id == app.id,
            Event.date == date)
            ).all()
        return event
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Unexpected error occured. Error: {ex}")
