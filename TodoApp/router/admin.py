from fastapi import APIRouter, status, Request
from model import model
from middlewares.db_middleware import db_dependency
from middlewares.admin_middleware import admin_dependency


router = APIRouter(prefix="/admin")   


"""
this route can only be accessed by the admin and
I created a middleware for authorizing this route only by the admin
"""
@router.get("/all/todo", status_code=status.HTTP_200_OK, description="route get all todos that exist in the system because it is an admin")
async def get_all_todos(admin: admin_dependency, db: db_dependency, req: Request):
    todo_for_admin = db.query(model.Todos).all()

    return todo_for_admin


@router.get("/all/users", status_code=status.HTTP_200_OK)
async def get_all_users(admin: admin_dependency, db: db_dependency, req: Request):
    all_users = db.query(model.Users).all()

    return all_users