from typing import Iterator
from sqlalchemy.orm import Session
from database import SessionLocal


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
