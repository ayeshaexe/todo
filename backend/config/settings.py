from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    NEON_DB_URL: str = "postgresql://neondb_owner:npg_69nHjwNzXBbd@ep-long-salad-a73u3ofv.ap-southeast-2.aws.neon.tech/neondb?sslmode=require"  # Default to SQLite for testing
    BETTER_AUTH_SECRET: str = "8ApAiAkyiQZg3XVId7GKjNyYXoFUw9vz"  # Default test secret
    BETTER_AUTH_URL: str = "https://todo-part2.vercel.app"

    class Config:
        env_file = ".env"

settings = Settings()