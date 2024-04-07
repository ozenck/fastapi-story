from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include cleaning dir in sys.path so that we can import from main.py

from apps.app.models import App
from apps.story.models import Story
from apps.event.models import Event
from apps.user.models import User

from main import application
from core.database import Base, get_db
from core.config import get_settings
from core.redis_handler import RedisSingleton

settings = get_settings()


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    settings.TEST_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=50,
    max_overflow=0
)


SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def insert_initial_data(db: SessionTesting):
    
    db.query(Event).delete()
    db.query(User).delete()
    db.query(Story).delete()
    db.query(App).delete()
    
    records = []
    for i in range(1,5):
        records.append(App(id=i, token=f"token{i}"))
    db.add_all(records)
    db.commit()

    story1 = Story(story_id=1, app_id=1, metadata_={"img": "image1.png"})
    story2 = Story(story_id=2, app_id=1, metadata_={"img": "image2.png"})
    story3 = Story(story_id=3, app_id=1, metadata_={"img": "image3.png"})
    story4 = Story(story_id=4, app_id=2, metadata_={"img": "image4.png"})
    story5 = Story(story_id=5, app_id=2, metadata_={"img": "image5.png"})

    records = []
    for i in range(1,4):
        records.append(User(id=i, name=f"user{i}", mail=f"user{i}@gmail.com"))
    db.add_all(records)
    db.commit()
    
    db.add_all([story1, story2, story3, story4, story5])
    db.commit()


class RedisMock:
    def cache(self):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            return wrapper
        return decorator


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)
    _app = application
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)

    # Insert initial data for test
    insert_initial_data(session)

    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def redis_cache(
    app: FastAPI,
) -> Generator[RedisMock, Any, None]:
    """
    Create a new FastAPI RedisMock that uses the `RedisSingleton` fixture to override
    """
    
    app.dependency_overrides[RedisSingleton] = RedisMock
    yield RedisMock


from unittest import mock

def mock_cache():
    mock.patch("core.redis_handler.RedisSingleton", lambda *args, **kwargs: lambda f: f).start()

def pytest_sessionstart(session):
    mock_cache()
