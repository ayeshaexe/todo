from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import sys
import os

# Add the backend directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from models.user import User
from models.task import Task

# Create database engine
engine = create_engine(settings.NEON_DB_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session