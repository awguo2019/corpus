import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import get_settings

# Prefer settings (env/.env) for configuration
settings = get_settings()
SQLALCHEMY_DATABASE_URL = settings.database_url or os.getenv(
    "DATABASE_URL",
    "postgresql://alan:corpus_password@localhost:5432/postgres",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()