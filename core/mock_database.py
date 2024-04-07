from sqlalchemy import create_engine
from core.config import get_settings
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import application as app
from core.database import get_db

settings = get_settings()

engine = create_engine(
    settings.TEST_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=50,
    max_overflow=0
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
