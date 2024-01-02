from fastapi import APIRouter, status
from schema import UserSchema
from middlewares.db_middleware import db_dependency
from model import model

router = APIRouter()


@router.get("/auth/login")
async def get_user():
    return {"user": "authenticated"}


@router.post("/auth/signup", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserSchema, db: db_dependency):
    user_data = model.Users(**data.dict())
    db.add(user_data)
    db.commit()
