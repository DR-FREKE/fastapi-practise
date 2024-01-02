from dataclasses import dataclass
from passlib.context import CryptContext


@dataclass
class PasswordHash:
    __bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @staticmethod
    def toHash(password: str) -> str:
        hashed_password = PasswordHash.__bcrypt_context.hash(password)
        return hashed_password

    async def comparePassword(self):
        pass
