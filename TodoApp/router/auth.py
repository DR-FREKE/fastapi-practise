import os
from fastapi import APIRouter, status, Depends, Request
from typing import Annotated
from schema import UserSchema, TokenSchema
from middlewares.db_middleware import db_dependency
from model import model
from fastapi.security import OAuth2PasswordRequestForm
from controllers.auth_controller import AuthController
from Error.customerror import BadRequestError
from services.password import PasswordHash
from jose import jwt
from datetime import timedelta, datetime


router = APIRouter()

SECRET_KEY = os.environ.get("SECRET_KEY") # I used both openssl to generate a key and echo -n 'key generated' | base64 to encrypt the key
ALGORITHM = "HS256"


def login_user(username: str, password: str, db, request: Request) -> str:
    user = db.query(model.Users).filter(model.Users.username == username).first()
    if not user:
        raise BadRequestError("Invalid Credentials")

    password_match = PasswordHash.comparePassword(supplied_password=password, stored_password=user.password)

    if not password_match:
        raise BadRequestError("Invalid Credentials")

    # create a JWT
    userJWT = create_access_token(user.username, user.id, timedelta(seconds=120))
    request.state.jwt = userJWT

    return {"access_token": userJWT, "token_type": "bearer"}


# create access token function
def create_access_token(username: str, user_id: int, expires: timedelta):
    
    # setup payload and expiration time for for JWT
    encode = {'sub': username, 'id': user_id}
    access_token_expires = datetime.utcnow() + expires
    encode.update({'exp': access_token_expires})

    # generate JWT token
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


@router.on_event("startup")
async def startup_event():
    db = db_dependency()
    AuthController.set_db_session(db)


@router.post("/auth/signup", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserSchema, db: db_dependency):
    user_data = model.Users(**data.dict())
    db.add(user_data)
    db.commit()


@router.post("/auth/token", status_code=status.HTTP_200_OK, response_model=TokenSchema) # the response_model is like an extra validation but for response...how the response should come. If the response doesn't match the way the TokenSchema was defined, an error will be thrown
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency, request: Request):
    return login_user(form_data.username, form_data.password, db, request)


# @router.get("/current-user", status_code=status.HTTP_200_OK)
# async def get_current_user(request: Request):
#     return {"jwt": request.session}