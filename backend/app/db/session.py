from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

DATABASE_URL = (f"postgresql+psycopg://{settings.DB_USER}:"
                f"{settings.DB_PASSWORD}@"
                f"{settings.DB_HOST}:"
                f"{settings.DB_PORT}/"
                f"{settings.DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()