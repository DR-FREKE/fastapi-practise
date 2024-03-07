from abc import ABC, abstractmethod, ABCMeta
from typing import List


class ErrorType:
    message: str
    field: str | None = None


class CustomError(Exception, ABC):
    @property
    @abstractmethod
    def statusCode(self) -> int:
        """property for status code"""

    def __init__(self, message: str):
        super().__init__(message)

    @abstractmethod
    def serializeError(self) -> List[ErrorType]:
        """abstract method for all classes"""


class NotFoundError(CustomError):
    statusCode: int = 404
    error: str = "Route Not Found"

    def __init__(self):
        super().__init__("Route Not Found")

    def serializeError(self) -> List[ErrorType]:
        return [{"message": self.error}]


class BadRequestError(CustomError):
    statusCode: int = 400
    __error: str

    def __init__(self, error: str):
        self.__error = error
        super().__init__("Bad Request Error")

    def serializeError(self) -> List[ErrorType]:
        return [{"message": self.__error}]


class DatabaseConnectionError(CustomError):
    statusCode: int = 500
    error: str = "An error occurred trying to connect to Database"

    def __init__(self):
        super().__init__("Error connecting to DB")

    def serializeError(self) -> List[ErrorType]:
        return [{"message": self.error}]


class RequestValidatorError(CustomError):
    statusCode: int = 400
    error: str = "Validation Error"
    
    def __init__(self):
        super().__init__("Validation Error")
    
    def serializeError(self) -> List[ErrorType]:
        return [{"message": self.error}]