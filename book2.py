from fastapi import FastAPI, Body, Request, Query, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from BookClass import BookClass, Author, Library, Type
from typing import List, Annotated
from Schema.BookSchema import BookModel, BookPatch
from uuid import uuid4
from middleware.errorhandler import errorHandler
from Error.customerror import CustomError

app: FastAPI = FastAPI(redoc_url="/book/api/v1")


@app.exception_handler(CustomError)
async def errorHandler(req: Request, err: CustomError):
    if isinstance(err, CustomError):
        return JSONResponse(status_code=err.statusCode, content={"error": err.serializeError()})


BOOKS: List[BookClass] = []

library = Library()


@app.get("/books/")
async def get_all_books(query: Request):
    if len(query.query_params.items()) == 0:
        return library.get_all_books()
    else:
        library.filter_book(list(query.query_params), query.query_params)


@app.get("/books/ratings/")
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    book = library.find_book_by_type(Type.RATINGS, book_rating)
    return book


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: str):
    book = library.find_book(book_id)
    print(book.__repr__())
    return book


@app.post("/books/add_books")
async def add_book(book_req: BookModel):
    book = BookClass(**book_req.dict())
    # use this if you wanted to do auto increment
    # BOOKS.append(find_book_id(book))

    # BOOKS.append(book)
    library.add_book(book)
    return book.getId()


@app.put("/books/{book_id}")
async def update_book(book_id: Annotated[str, Path(min_length=1)], book_data: BookModel):
    book = BookClass(**book_data.dict())
    edited_book = library.edit_book(book=book, book_id=book_id)
    return edited_book


@app.patch("/books/{book_id}")
async def patch_a_book(book_id: Annotated[str, Path(min_length=1)], book_data: BookPatch):
    stored_book = library.find_book(book_id).__repr__()
    stored_book_model = BookPatch(**stored_book)
    print(stored_book_model)
    update_data = book_data.dict(
        exclude_unset=True)  # get the request data and convert to dictionary, also use the exclude_unset not make any field compulsory

    """update data in the model"""
    updated_data = stored_book_model.copy(update=update_data)
    return jsonable_encoder(updated_data)


@app.delete("/books/delete/{book_id}")
async def delete_book(book_id: Annotated[str, Path(min_length=1)]):
    return library.delete_book(book_id)


# use this function if you were doing auto increment like (1, 2, 3, 4, 5 ...). We actually don't need it because we're using UUID
def find_book_id(book: BookClass):
    id = uuid4().hex if len(library.get_all_books()) == 0 else uuid4().hex or library.get_all_books()[
        -1].getId() + 1  # using tie-nary operator
    book.setId(id)
    #
    # if len(BOOKS) > 0:
    #     id = BOOKS[-1].getId() + 1
    #     book.setId(id)
    # else:
    #     book.setId(1)
    return book


""" NOTE: pydantic is the framework that we use for the validation of our data. From pydantic, 
we get BaseModel and BaseModel is what we use for our model i.e the object coming in from the request;
we use this to set like a structure for our object field validation"""
