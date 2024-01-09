from fastapi import APIRouter, status, Depends
from typing import Annotated
from schema import UserSchema
from middlewares.db_middleware import db_dependency
from model import model
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/auth/signup", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserSchema, db: db_dependency):
    user_data = model.Users(**data.dict())
    db.add(user_data)
    db.commit()


@router.post("/auth/token", status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return form_data.username
