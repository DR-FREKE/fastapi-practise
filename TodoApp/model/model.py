from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, event
from services.password import PasswordHash


# Quick Note: delete command for sql -> delete from todos where id = 4. update command is -> update todos set column = value where id = 4

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")


@event.listens_for(Users, 'before_insert')
def hashPassword(mapper, connect, target):
    target.password = PasswordHash.toHash(target.password)
    print(PasswordHash.toHash(target.password))

