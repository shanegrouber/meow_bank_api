import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from meow_bank.core.config import settings

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./meow_bank.db")

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from meow_bank.db import models  # noqa: F401 - required for models to be available

    Base.metadata.create_all(bind=engine)
