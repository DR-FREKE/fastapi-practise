from typing import List, TypedDict, Dict, Annotated
from fastapi import FastAPI, Request, Response, Body, Query, Path
from fastapi.encoders import jsonable_encoder
import requests
import matplotlib.pyplot as plt
import numpy as np
from pydantic import BaseModel, Field, Required
from uuid import UUID

app: FastAPI = FastAPI(redoc_url="/book_docs")


class BookClass(TypedDict):
    title: str
    author: str
    category: str


class BookModel(BaseModel):
    # id: UUID
    title: str = Field(min_length=1)
    author: str = Field(default="Solomon Ndifereke")
    category: str = Field(default="Technology")


BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Two", "category": "math"}
]

"""create function and expose to an endpoint"""


@app.get("/api-endpoint")
async def first_api() -> dict[str, str]:
    return {"message": "Hello World!"}


# this is known as a static path parameter
@app.get("/books")
async def get_all_books() -> List[BookClass]:
    return BOOKS


# this is known as a dynamic path parameter
@app.get("/books/{book_title}")
# if you wanted a number as the parameter, remove the type hint of str from the get_a_book method and replace with int
async def get_a_book(book_title: str = Path(alias="")) -> BookClass:
    title: str = book_title.casefold().replace("_", " ")
    book: BookClass
    for book in BOOKS:
        if book.get("title").casefold() == title.casefold():
            return book


@app.get("/books/author/{author_name}")
async def get_books_by_author(author_name: str) -> List[BookClass]:
    books_by_author = filter(lambda book: book.get("author").casefold() == author_name.casefold(), BOOKS)
    return list(books_by_author)


@app.get("/books/")
async def get_books_by_category(category: str | int) -> List[BookClass]:  # you could also use Union(int, str)
    books_by_category = filter(lambda book_cat: book_cat.get("category").casefold() == category.casefold(), BOOKS)
    return list(books_by_category)


# another way to do the filter but space complexity is huge is:
@app.get("/books/{book_title}/")
async def get_books_by_author(book_title: str, author_name: str) -> List[BookClass]:
    new_book_arr = []
    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold() and \
                book.get("title").casefold() == book_title.casefold():
            new_book_arr.append(book)
    return new_book_arr


# old method of adding validation to query params
@app.get("/books/my_author/{author}/")
async def get_books_query_author(author: str, book_title: str | None = Query(default=Required, max_length=10)) -> List[
    BookClass]:
    filtered_books = filter(lambda book: book.get("author").casefold() == author.casefold() and \
                                         book.get("title").casefold() == book_title.casefold(), BOOKS)
    return list(filtered_books)


# new method of adding validation to query params
@app.get("/author/{author_name}/")
async def get_author_by_query_string(author_name: str, category: Annotated[str | None, Query(max_length=10)] = None) -> \
        List[BookClass]:
    filtered_by_author = filter(lambda book: book.get("author").casefold() == author_name.casefold() and \
                                             book.get("category").casefold() == category.casefold(), BOOKS)
    return list(filtered_by_author)


@app.post("/books/create_book")
async def create_book(new_book: BookModel = Body()):
    BOOKS.append(dict(new_book))
    return BOOKS


@app.put("/books/{book_title}")
async def update_book(book_title: str, update_book_data: BookModel = Body()) -> BookClass:
    result: BookClass = None
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS[i] = update_book_data
            result = BOOKS[i]
    return result


@app.patch("/books/{book_title}")
async def update_book_by_patch(book_title: str, patch_book: BookModel = Body()) -> BookClass:
    result: BookClass
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            stored_book = BOOKS[i]
            stored_book_model = BookModel(**stored_book) # the ** operator is a spread operator for function/method argument spread
            updated_item = patch_book.dict(exclude_unset=True)
            update_data = stored_book_model.copy(update=updated_item)
            BOOKS[i] = jsonable_encoder(update_data)
            result = BOOKS[i]
    return result


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            result = {"message": f"book with {book_title} title has been deleted!"}
            break
        else:
            result = {"message": f"{book_title} does not exist"}
    return result


# this route allows you get multiple query string; thanks to the Request from fastapi
@app.get("/books/all_query/")
async def get_book_by_query(req: Request):
    req.session = {"jwt": "some"}
    query = req.query_params.items()
    print(query)


@app.get("/external-books")
async def get_external_books():
    try:
        header = {"Authorization": "8e5e787c69f486b7e610eb23719a4e656d7aa410"}
        response = requests.get("https://api.github.com/users/VikParuchuri/orgs", headers=header)
        if response.status_code == 200:
            return response.json()
        else:
            raise IOError
    except IOError:
        print("error occurred")


@app.get("/plot-graph")
async def plot_graph():
    x_axis = np.linspace(0, 2 * np.pi, 200)
    y_axis = np.sin(x_axis)

    # fig, graph = plt.subplots()
    # graph.plot(x_axis, y_axis)
    # plt.show()
    plt.plot(x_axis, y_axis)
    plt.show()
