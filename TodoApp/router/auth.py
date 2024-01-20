from fastapi import APIRouter, status, Depends
from typing import Annotated
from schema import UserSchema
from middlewares.db_middleware import db_dependency
from model import model
from fastapi.security import OAuth2PasswordRequestForm
from controllers.auth_controller import AuthController


router = APIRouter()


# def login_user(username: str, password: str, db) -> None:
#     user = db.query(model.Users).filter(model.Users.username == username).first()
#     if not user:
#         raise BadRequestError("Invalid Credentials")

#     password_match = PasswordHash.comparePassword(supplied_password=password, stored_password=user.password)

#     if not password_match:
#         raise BadRequestError("Invalid Credentials")

#     # create a JWT
#     return "JWT"

@router.on_event("startup")
async def startup_event():
    db = db_dependency()
    AuthController.set_db_session(db)


@router.post("/auth/signup", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserSchema, db: db_dependency):
    user_data = model.Users(**data.dict())
    db.add(user_data)
    db.commit()


@router.post("/auth/token", status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return AuthController.login_user(form_data.username, form_data.password)
