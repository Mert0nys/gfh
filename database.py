from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from schemas import Settings

DATABASE_URL = "postgresql://postgres:Gamemode1@localhost:5432/bookers"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

settings = Settings()

def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

