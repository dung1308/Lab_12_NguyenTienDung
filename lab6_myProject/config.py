from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Production Agent"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    # API Settings
    agent_api_key: str = "dev-key-123"
    rate_limit_per_minute: int = 10
    daily_budget_usd: float = 10.0
    
    # Infrastructure
    REDIS_URL: str = "redis://localhost:6379"
    port: int = 8000
    host: str = "0.0.0.0"
    
    class Config:
        # Thứ tự này giúp .env.local ghi đè các giá trị trong .env (nếu có cả hai)
        env_file = (".env", ".env.local")

settings = Settings()