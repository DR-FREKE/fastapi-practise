from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database.database import SessionLocal


def get_db():
    """
    Dependency function to get a database session.

    Yields:
        Session: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# This middleware provides a database session to the API endpoints.
# It ensures proper handling of the database session lifecycle.