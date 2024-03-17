import os
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, Request
from Error.customerror import NotAuthorizedError
from jose import jwt, JWTError


SECRET_KEY = os.environ.get("SECRET_KEY") # I used both openssl to generate a key and echo -n 'key generated' | base64 to encrypt the key
ALGORITHM = os.environ.get("APP_ALGORITHM")


# setup bearer var...it is used to setup what the client will pass in the header. the token is going to have the JWT token
oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/token', auto_error=False) ## auto_error disables the default UnAuthenticated error given by OAuth2PasswordBearer package


# this is a middleware for authorizing endpoints
async def authorize(token: Annotated[str, Depends(oauth_bearer)], req: Request):
    if not token:
        raise NotAuthorizedError("UnAuthorized Request")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')

        if username is None or user_id is None:
            raise NotAuthorizedError('UnAuthorized Request')
        
        # return {**payload.dict()}
        req.state.currentUser = payload
        print(req)

        return {"username": username, "id": user_id, 'role': role}
    except JWTError:
        raise NotAuthorizedError('UnAuthorized Request')
    

auth = Annotated[dict, Depends(authorize)]
