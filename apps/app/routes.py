from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.orm import Session
from core.database import get_db
from jose import jwt
from apps.app.models import App
from core.redis_handler import RedisSingleton

SECRET_KEY = "this is ozenc's secret key for storyly demo project"

app_router = APIRouter(
    prefix="/app",
    tags=["App"],
    responses={404: {"description": "Not found"}},
)

redis_cache = RedisSingleton()

async def app_to_dict(app_instance):
    app_dict = {
        "id": app_instance.id,
        "token": app_instance.token,
    }
    return app_dict

@app_router.get("/", status_code=status.HTTP_200_OK)
@redis_cache.cache(timeout=60)
async def get_apps(request: Request, db: Session = Depends(get_db)):
    result = db.query(App).all()
    return [await app_to_dict(app) for app in result]
