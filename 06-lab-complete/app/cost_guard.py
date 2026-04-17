import redis
import time
from fastapi import HTTPException
from app.config import settings

r = redis.from_url(settings.REDIS_URL)

def check_budget(user_id: str):
    today = time.strftime("%Y-%m-%d")
    key = f"cost:{user_id}:{today}"
    current_cost = float(r.get(key) or 0)
    
    if current_cost >= settings.daily_budget_usd:
        raise HTTPException(
            status_code=402, 
            detail=f"Daily budget of ${settings.daily_budget_usd} exhausted."
        )

def update_cost(user_id: str, cost: float):
    today = time.strftime("%Y-%m-%d")
    r.incrbyfloat(f"cost:{user_id}:{today}", cost)