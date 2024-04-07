from fastapi import FastAPI
from core.database import Base, engine
from apps.app.routes import app_router
from apps.story.routes import stories_router
from apps.event.routes import events_router
from scripts.initial_data import create_initial_data
from core.database import SessionLocal

Base.metadata.create_all(bind=engine)

application = FastAPI()
application.include_router(app_router)
application.include_router(stories_router)
application.include_router(events_router)

async def startup_event():
    db = SessionLocal()
    try:
        create_initial_data(db)
    finally:
        db.close()

# Automatically insert sample data to App, Story, User tables on the fastapi load.
application.router.add_event_handler("startup", startup_event)
