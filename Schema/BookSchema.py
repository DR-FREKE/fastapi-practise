from pydantic import BaseModel, Field, UUID4
from uuid import UUID


class AuthorModel(BaseModel):
    name: str = Field(min_length=1)
    title: str = Field(min_length=1, default="MR")
    age: int


class AuthorPatch(AuthorModel):
    name: str = None
    title: str = None
    age: int = None


class BookModel(BaseModel):
    # id: int | UUID | None
    title: str = Field(min_length=3)
    author: AuthorModel
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    class Config:
        schema_extra = {
            "example": {
                "title": "A tales by the Moon Light",
                "author": {
                    "name": "Solomon Ndifereke",
                    "title": "MR",
                    "age": 40
                },
                "description": "A description of the book",
                "rating": 5
            }
        }


class BookPatch(BookModel):
    title: str = None
    author: AuthorPatch = None
    description: str = None
    rating: int = None
