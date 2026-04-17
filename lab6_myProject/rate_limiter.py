import redis
import time
from fastapi import HTTPException
from app.config import settings

r = redis.from_url(settings.REDIS_URL)

def check_rate_limit(user_id: str):
    now = time.time()
    key = f"rate_limit:{user_id}"
    window = 60
    limit = settings.rate_limit_per_minute

    r.zremrangebyscore(key, 0, now - window)
    current_count = r.zcard(key)
    
    if current_count >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {limit} req/min"
        )
    
    r.zadd(key, {str(now): now})
    r.expire(key, window)