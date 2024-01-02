from fastapi.exceptions import RequestValidationError
from fastapi import Request, Response, HTTPException, status


async def validateRequest(request: Request, err: RequestValidationError):
    if err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=err)
