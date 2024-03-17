from fastapi import FastAPI, Request
from model import model
from database.database import engine
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from router import auth, todo, admin

from dotenv import load_dotenv

load_dotenv()


from Error.customerror import CustomError

app = FastAPI(docs_url='/todo_docs', redoc_url='/todo_redoc')

model.Base.metadata.create_all(bind=engine)  # note: this only runs when there's no database file created.
# So if todos.db does not exist, then this will create it using everything from database.py file and model.py file,
# and bind it to the engine for us to be able to query the db

app.include_router(auth.router, prefix="", tags=['auth'])
app.include_router(todo.router, prefix="", tags=["todos"])
app.include_router(admin.router, tags=["admin"])


@app.exception_handler(RequestValidationError)
@app.exception_handler(CustomError)
async def errorHandler(req: Request, err: CustomError):
    if isinstance(err, CustomError):
        return JSONResponse(status_code=err.statusCode, content={"error": err.serializeError()})
