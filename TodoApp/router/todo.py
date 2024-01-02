from fastapi import APIRouter, Path, status, Request
from typing import Annotated
from model import model
from schema import TodoSchema, TodoSchemaPatch
from Error.customerror import NotFoundError
from middlewares.db_middleware import db_dependency

router = APIRouter()


@router.get("/todo")
async def get_all_todos(db: db_dependency, req: Request):
    print(req.currentUser)
    return db.query(model.Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(todo_id: Annotated[int, Path(gt=0)], db: db_dependency):
    todo_model = db.query(model.Todos).filter(model.Todos.id == todo_id).first()

    if todo_model is None:
        # throw exception
        raise NotFoundError
    return todo_model


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(todo: TodoSchema, db: db_dependency):
    todo_data = model.Todos(**todo.dict())
    db.add(todo_data)
    db.commit()

    return {"message": "added todo", "data": todo_data}


@router.patch("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(todo_id: Annotated[int, Path(gt=0)], todo: TodoSchemaPatch, db: db_dependency):
    find_todo = db.query(model.Todos).filter(model.Todos.id == todo_id).first()
    if find_todo is None:
        raise NotFoundError()

    # update the todo
    update_data = todo.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(find_todo, key, value)
    db.add(find_todo)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: Annotated[int, Path(gt=0)], db: db_dependency):
    find_todo = db.query(model.Todos).filter(model.Todos.id == todo_id).first()
    if find_todo is None:
        raise NotFoundError()

    # delete the todo
    db.delete(find_todo)
    db.commit()
