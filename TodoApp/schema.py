from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class TodoSchema(BaseModel):
    title: str = Field(min_length=3)
    description: Annotated[str, Field(min_length=3, max_length=100)]
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)


class TodoSchemaPatch(BaseModel):
    title: Annotated[str, Field(min_length=3)] = None
    description: Annotated[str, Field(min_length=3, max_length=100)] = None
    priority: Annotated[int, Field(gt=0, lt=6)] = None
    complete: bool

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    email: EmailStr = Field(examples="solomonndi96@gmail.com")
    username: str = Field(min_length=5)
    first_name: str = Field()
    last_name: str = Field()
    password: str = Field()
    role: Annotated[str, Field()] = None

    class Config:
        schema_extra = {
            "example": {
                "email": "solomonndi96@gmail.com",
                "username": "solomonndi96",
                "first_name": "Ndifereke",
                "last_name": "Solomon",
                "password": "Solomon100",
            }
        }


class TokenSchema(BaseModel):
    access_token: str
    token_type: str