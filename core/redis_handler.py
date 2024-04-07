import redis
import json
import functools
from core.config import get_settings

settings = get_settings()

class RedisSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            print("instance yok yeni olustur")
            cls._instance = super(RedisSingleton, cls).__new__(cls)
            # Initialize Redis client
            cls._instance.client = redis.Redis(
                host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True
            )
        return cls._instance

    def cache(self, timeout: int = 60):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):

                request = kwargs.get("request")
                if not request:
                    raise ValueError("Request object not found")
                if "testserver" == request.url.hostname:
                    return await func(*args, **kwargs)
                cache_key = str(request.url)
                
                cached_data = self.client.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
                
                result = await func(*args, **kwargs)
                if isinstance(result, dict) or isinstance(result, list):
                    self.client.set(cache_key, json.dumps(result), ex=timeout)
                
                return result

            return wrapper
        return decorator
