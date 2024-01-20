from dataclasses import dataclass
from passlib.context import CryptContext


@dataclass
class PasswordHash:
    __bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def toHash(cls, password: str) -> str:
        hashed_password = cls.__bcrypt_context.hash(password)
        return hashed_password

    @classmethod
    def comparePassword(cls, stored_password: str, supplied_password: str):
        if not cls.__bcrypt_context.verify(supplied_password, stored_password):
            return False
        return True
