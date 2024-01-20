from Error.customerror import BadRequestError
from services.password import PasswordHash
from model import model
from middlewares.db_middleware import db_dependency


class AuthController:
    db_session= None

    @classmethod
    def set_db_session(cls, db):
        cls.db_session = db

    @classmethod
    def login_user(cls, username: str, password: str) -> None:
        if cls.db_session is None:
            raise Exception("Error with database initialization")

        user = cls.db_session.query(model.Users).filter(model.Users.username == username).first()
        
        if not user:
            raise BadRequestError("Invalid Credentials")
        
        password_match = PasswordHash.comparePassword(stored_password=user.password, supplied_password=password)
        
        if not password_match:
            raise BadRequestError("Invalid Credentials")
        
        # create a JWT
        return "JWT"